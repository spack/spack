# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module contains functions related to finding compilers on the
system and configuring Spack to use multiple compilers.
"""
import collections
import itertools
import multiprocessing.pool
import os
from typing import Dict, List, Optional, Tuple

import archspec.cpu

import llnl.util.filesystem as fs
import llnl.util.lang
import llnl.util.tty as tty

import spack.compiler
import spack.config
import spack.error
import spack.operating_systems
import spack.paths
import spack.platforms
import spack.spec
import spack.version
from spack.util.environment import get_path
from spack.util.naming import mod_to_class

_path_instance_vars = ["cc", "cxx", "f77", "fc"]
_flags_instance_vars = ["cflags", "cppflags", "cxxflags", "fflags"]
_other_instance_vars = [
    "modules",
    "operating_system",
    "environment",
    "implicit_rpaths",
    "extra_rpaths",
]

# TODO: Caches at module level make it difficult to mock configurations in
# TODO: unit tests. It might be worth reworking their implementation.
#: cache of compilers constructed from config data, keyed by config entry id.
_compiler_cache: Dict[str, "spack.compiler.Compiler"] = {}

_compiler_to_pkg = {
    "clang": "llvm+clang",
    "oneapi": "intel-oneapi-compilers",
    "rocmcc": "llvm-amdgpu",
    "intel@2020:": "intel-oneapi-compilers-classic",
    "arm": "acfl",
}

# TODO: generating this from the previous dict causes docs errors
package_name_to_compiler_name = {
    "llvm": "clang",
    "intel-oneapi-compilers": "oneapi",
    "llvm-amdgpu": "rocmcc",
    "intel-oneapi-compilers-classic": "intel",
    "acfl": "arm",
}


def pkg_spec_for_compiler(cspec):
    """Return the spec of the package that provides the compiler."""
    for spec, package in _compiler_to_pkg.items():
        if cspec.satisfies(spec):
            spec_str = "%s@%s" % (package, cspec.versions)
            break
    else:
        spec_str = str(cspec)
    return spack.spec.parse_with_version_concrete(spec_str)


def _auto_compiler_spec(function):
    def converter(cspec_like, *args, **kwargs):
        if not isinstance(cspec_like, spack.spec.CompilerSpec):
            cspec_like = spack.spec.CompilerSpec(cspec_like)
        return function(cspec_like, *args, **kwargs)

    return converter


def _to_dict(compiler):
    """Return a dict version of compiler suitable to insert in YAML."""
    d = {}
    d["spec"] = str(compiler.spec)
    d["paths"] = dict((attr, getattr(compiler, attr, None)) for attr in _path_instance_vars)
    d["flags"] = dict((fname, " ".join(fvals)) for fname, fvals in compiler.flags.items())
    d["flags"].update(
        dict(
            (attr, getattr(compiler, attr, None))
            for attr in _flags_instance_vars
            if hasattr(compiler, attr)
        )
    )
    d["operating_system"] = str(compiler.operating_system)
    d["target"] = str(compiler.target)
    d["modules"] = compiler.modules or []
    d["environment"] = compiler.environment or {}
    d["extra_rpaths"] = compiler.extra_rpaths or []
    if compiler.enable_implicit_rpaths is not None:
        d["implicit_rpaths"] = compiler.enable_implicit_rpaths

    if compiler.alias:
        d["alias"] = compiler.alias

    return {"compiler": d}


def get_compiler_config(scope=None, init_config=True):
    """Return the compiler configuration for the specified architecture."""

    config = spack.config.get("compilers", scope=scope) or []
    if config or not init_config:
        return config

    merged_config = spack.config.get("compilers")
    if merged_config:
        return config

    _init_compiler_config(scope=scope)
    config = spack.config.get("compilers", scope=scope)
    return config


def _init_compiler_config(*, scope):
    """Compiler search used when Spack has no compilers."""
    compilers = find_compilers()
    compilers_dict = []
    for compiler in compilers:
        compilers_dict.append(_to_dict(compiler))
    spack.config.set("compilers", compilers_dict, scope=scope)


def compiler_config_files():
    config_files = list()
    config = spack.config.CONFIG
    for scope in config.file_scopes:
        name = scope.name
        compiler_config = config.get("compilers", scope=name)
        if compiler_config:
            config_files.append(config.get_config_filename(name, "compilers"))
    return config_files


def add_compilers_to_config(compilers, scope=None, init_config=True):
    """Add compilers to the config for the specified architecture.

    Arguments:
        compilers: a list of Compiler objects.
        scope: configuration scope to modify.
    """
    compiler_config = get_compiler_config(scope, init_config)
    for compiler in compilers:
        if not compiler.cc:
            tty.debug(f"{compiler.spec} does not have a C compiler")
        if not compiler.cxx:
            tty.debug(f"{compiler.spec} does not have a C++ compiler")
        if not compiler.f77:
            tty.debug(f"{compiler.spec} does not have a Fortran77 compiler")
        if not compiler.fc:
            tty.debug(f"{compiler.spec} does not have a Fortran compiler")
        compiler_config.append(_to_dict(compiler))
    spack.config.set("compilers", compiler_config, scope=scope)


@_auto_compiler_spec
def remove_compiler_from_config(compiler_spec, scope=None):
    """Remove compilers from configuration by spec.

    If scope is None, all the scopes are searched for removal.

    Arguments:
        compiler_spec: compiler to be removed
        scope: configuration scope to modify
    """
    candidate_scopes = [scope]
    if scope is None:
        candidate_scopes = spack.config.CONFIG.scopes.keys()

    removal_happened = False
    for current_scope in candidate_scopes:
        removal_happened |= _remove_compiler_from_scope(compiler_spec, scope=current_scope)

    return removal_happened


def _remove_compiler_from_scope(compiler_spec, scope):
    """Removes a compiler from a specific configuration scope.

    Args:
        compiler_spec: compiler to be removed
        scope: configuration scope under consideration

    Returns:
         True if one or more compiler entries were actually removed, False otherwise
    """
    assert scope is not None, "a specific scope is needed when calling this function"
    compiler_config = get_compiler_config(scope)
    filtered_compiler_config = [
        compiler_entry
        for compiler_entry in compiler_config
        if not spack.spec.parse_with_version_concrete(
            compiler_entry["compiler"]["spec"], compiler=True
        ).satisfies(compiler_spec)
    ]

    if len(filtered_compiler_config) == len(compiler_config):
        return False

    # We need to preserve the YAML type for comments, hence we are copying the
    # items in the list that has just been retrieved
    compiler_config[:] = filtered_compiler_config
    spack.config.set("compilers", compiler_config, scope=scope)
    return True


def all_compilers_config(scope=None, init_config=True):
    """Return a set of specs for all the compiler versions currently
    available to build with.  These are instances of CompilerSpec.
    """
    return get_compiler_config(scope, init_config)


def all_compiler_specs(scope=None, init_config=True):
    # Return compiler specs from the merged config.
    return [
        spack.spec.parse_with_version_concrete(s["compiler"]["spec"], compiler=True)
        for s in all_compilers_config(scope, init_config)
    ]


def find_compilers(
    path_hints: Optional[List[str]] = None, *, mixed_toolchain=False
) -> List["spack.compiler.Compiler"]:
    """Return the list of compilers found in the paths given as arguments.

    Args:
        path_hints: list of path hints where to look for. A sensible default based on the ``PATH``
            environment variable will be used if the value is None
        mixed_toolchain: allow mixing compilers from different toolchains if otherwise missing for
            a certain language
    """
    if path_hints is None:
        path_hints = get_path("PATH")
    default_paths = fs.search_paths_for_executables(*path_hints)

    # To detect the version of the compilers, we dispatch a certain number
    # of function calls to different workers. Here we construct the list
    # of arguments for each call.
    arguments = []
    for o in all_os_classes():
        search_paths = getattr(o, "compiler_search_paths", default_paths)
        arguments.extend(arguments_to_detect_version_fn(o, search_paths))

    # Here we map the function arguments to the corresponding calls
    tp = multiprocessing.pool.ThreadPool()
    try:
        detected_versions = tp.map(detect_version, arguments)
    finally:
        tp.close()

    def valid_version(item: Tuple[Optional[DetectVersionArgs], Optional[str]]) -> bool:
        value, error = item
        if error is None:
            return True
        try:
            # This will fail on Python 2.6 if a non ascii
            # character is in the error
            tty.debug(error)
        except UnicodeEncodeError:
            pass
        return False

    def remove_errors(
        item: Tuple[Optional[DetectVersionArgs], Optional[str]]
    ) -> DetectVersionArgs:
        value, _ = item
        assert value is not None
        return value

    return make_compiler_list(
        [remove_errors(detected) for detected in detected_versions if valid_version(detected)],
        mixed_toolchain=mixed_toolchain,
    )


def find_new_compilers(
    path_hints: Optional[List[str]] = None,
    scope: Optional[str] = None,
    *,
    mixed_toolchain: bool = False,
):
    """Same as ``find_compilers`` but return only the compilers that are not
    already in compilers.yaml.

    Args:
        path_hints: list of path hints where to look for. A sensible default based on the ``PATH``
            environment variable will be used if the value is None
        scope: scope to look for a compiler. If None consider the merged configuration.
        mixed_toolchain: allow mixing compilers from different toolchains if otherwise missing for
            a certain language
    """
    compilers = find_compilers(path_hints, mixed_toolchain=mixed_toolchain)

    return select_new_compilers(compilers, scope)


def select_new_compilers(compilers, scope=None):
    """Given a list of compilers, remove those that are already defined in
    the configuration.
    """
    compilers_not_in_config = []
    for c in compilers:
        arch_spec = spack.spec.ArchSpec((None, c.operating_system, c.target))
        same_specs = compilers_for_spec(c.spec, arch_spec, scope=scope, init_config=False)
        if not same_specs:
            compilers_not_in_config.append(c)

    return compilers_not_in_config


def supported_compilers() -> List[str]:
    """Return a set of names of compilers supported by Spack.

    See available_compilers() to get a list of all the available
    versions of supported compilers.
    """
    # Hack to be able to call the compiler `apple-clang` while still
    # using a valid python name for the module
    return sorted(all_compiler_names())


def supported_compilers_for_host_platform() -> List[str]:
    """Return a set of compiler class objects supported by Spack
    that are also supported by the current host platform
    """
    host_plat = spack.platforms.real_host()
    return supported_compilers_for_platform(host_plat)


def supported_compilers_for_platform(platform: spack.platforms.Platform) -> List[str]:
    """Return a set of compiler class objects supported by Spack
    that are also supported by the provided platform

    Args:
        platform (str): string representation of platform
            for which compiler compatability should be determined
    """
    return [
        name
        for name in supported_compilers()
        if class_for_compiler_name(name).is_supported_on_platform(platform)
    ]


def all_compiler_names() -> List[str]:
    def replace_apple_clang(name):
        return name if name != "apple_clang" else "apple-clang"

    return [replace_apple_clang(name) for name in all_compiler_module_names()]


def all_compiler_module_names() -> List[str]:
    return [name for name in llnl.util.lang.list_modules(spack.paths.compilers_path)]


@_auto_compiler_spec
def supported(compiler_spec):
    """Test if a particular compiler is supported."""
    return compiler_spec.name in supported_compilers()


@_auto_compiler_spec
def find(compiler_spec, scope=None, init_config=True):
    """Return specs of available compilers that match the supplied
    compiler spec.  Return an empty list if nothing found."""
    return [c for c in all_compiler_specs(scope, init_config) if c.satisfies(compiler_spec)]


@_auto_compiler_spec
def find_specs_by_arch(compiler_spec, arch_spec, scope=None, init_config=True):
    """Return specs of available compilers that match the supplied
    compiler spec.  Return an empty list if nothing found."""
    return [c.spec for c in compilers_for_spec(compiler_spec, arch_spec, scope, True, init_config)]


def all_compilers(scope=None, init_config=True):
    config = get_compiler_config(scope, init_config=init_config)
    compilers = list()
    for items in config:
        items = items["compiler"]
        compilers.append(_compiler_from_config_entry(items))
    return compilers


@_auto_compiler_spec
def compilers_for_spec(
    compiler_spec, arch_spec=None, scope=None, use_cache=True, init_config=True
):
    """This gets all compilers that satisfy the supplied CompilerSpec.
    Returns an empty list if none are found.
    """
    if use_cache:
        config = all_compilers_config(scope, init_config)
    else:
        config = get_compiler_config(scope, init_config)

    matches = set(find(compiler_spec, scope, init_config))
    compilers = []
    for cspec in matches:
        compilers.extend(get_compilers(config, cspec, arch_spec))
    return compilers


def compilers_for_arch(arch_spec, scope=None):
    config = all_compilers_config(scope)
    return list(get_compilers(config, arch_spec=arch_spec))


def compiler_specs_for_arch(arch_spec, scope=None):
    return [c.spec for c in compilers_for_arch(arch_spec, scope)]


class CacheReference:
    """This acts as a hashable reference to any object (regardless of whether
    the object itself is hashable) and also prevents the object from being
    garbage-collected (so if two CacheReference objects are equal, they
    will refer to the same object, since it will not have been gc'ed since
    the creation of the first CacheReference).
    """

    def __init__(self, val):
        self.val = val
        self.id = id(val)

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return isinstance(other, CacheReference) and self.id == other.id


def compiler_from_dict(items):
    cspec = spack.spec.parse_with_version_concrete(items["spec"], compiler=True)
    os = items.get("operating_system", None)
    target = items.get("target", None)

    if not ("paths" in items and all(n in items["paths"] for n in _path_instance_vars)):
        raise InvalidCompilerConfigurationError(cspec)

    cls = class_for_compiler_name(cspec.name)

    compiler_paths = []
    for c in _path_instance_vars:
        compiler_path = items["paths"][c]
        if compiler_path != "None":
            compiler_paths.append(compiler_path)
        else:
            compiler_paths.append(None)

    mods = items.get("modules")
    if mods == "None":
        mods = []

    alias = items.get("alias", None)
    compiler_flags = items.get("flags", {})
    environment = items.get("environment", {})
    extra_rpaths = items.get("extra_rpaths", [])
    implicit_rpaths = items.get("implicit_rpaths", None)

    # Starting with c22a145, 'implicit_rpaths' was a list. Now it is a
    # boolean which can be set by the user to disable all automatic
    # RPATH insertion of compiler libraries
    if implicit_rpaths is not None and not isinstance(implicit_rpaths, bool):
        implicit_rpaths = None

    return cls(
        cspec,
        os,
        target,
        compiler_paths,
        mods,
        alias,
        environment,
        extra_rpaths,
        enable_implicit_rpaths=implicit_rpaths,
        **compiler_flags,
    )


def _compiler_from_config_entry(items):
    """Note this is intended for internal use only. To avoid re-parsing
    the same config dictionary this keeps track of its location in
    memory. If you provide the same dictionary twice it will return
    the same Compiler object (regardless of whether the dictionary
    entries have changed).
    """
    config_id = CacheReference(items)
    compiler = _compiler_cache.get(config_id, None)

    if compiler is None:
        compiler = compiler_from_dict(items)
        _compiler_cache[config_id] = compiler

    return compiler


def get_compilers(config, cspec=None, arch_spec=None):
    compilers = []

    for items in config:
        items = items["compiler"]

        # NOTE: in principle this should be equality not satisfies, but config can still
        # be written in old format gcc@10.1.0 instead of gcc@=10.1.0.
        if cspec and not cspec.satisfies(items["spec"]):
            continue

        # If an arch spec is given, confirm that this compiler
        # is for the given operating system
        os = items.get("operating_system", None)
        if arch_spec and os != arch_spec.os:
            continue

        # If an arch spec is given, confirm that this compiler
        # is for the given target. If the target is 'any', match
        # any given arch spec. If the compiler has no assigned
        # target this is an old compiler config file, skip this logic.
        target = items.get("target", None)

        try:
            current_target = archspec.cpu.TARGETS[str(arch_spec.target)]
            family = str(current_target.family)
        except KeyError:
            # TODO: Check if this exception handling makes sense, or if we
            # TODO: need to change / refactor tests
            family = arch_spec.target
        except AttributeError:
            assert arch_spec is None

        if arch_spec and target and (target != family and target != "any"):
            # If the family of the target is the family we are seeking,
            # there's an error in the underlying configuration
            if archspec.cpu.TARGETS[target].family == family:
                msg = (
                    'the "target" field in compilers.yaml accepts only '
                    'target families [replace "{0}" with "{1}"'
                    ' in "{2}" specification]'
                )
                msg = msg.format(str(target), family, items.get("spec", "??"))
                raise ValueError(msg)
            continue

        compilers.append(_compiler_from_config_entry(items))

    return compilers


@_auto_compiler_spec
def compiler_for_spec(compiler_spec, arch_spec):
    """Get the compiler that satisfies compiler_spec.  compiler_spec must
    be concrete."""
    assert compiler_spec.concrete
    assert arch_spec.concrete

    compilers = compilers_for_spec(compiler_spec, arch_spec=arch_spec)
    if len(compilers) < 1:
        raise NoCompilerForSpecError(compiler_spec, arch_spec.os)
    if len(compilers) > 1:
        msg = "Multiple definitions of compiler %s " % compiler_spec
        msg += "for architecture %s:\n %s" % (arch_spec, compilers)
        tty.debug(msg)
    return compilers[0]


@_auto_compiler_spec
def get_compiler_duplicates(compiler_spec, arch_spec):
    config = spack.config.CONFIG

    scope_to_compilers = {}
    for scope in config.scopes:
        compilers = compilers_for_spec(
            compiler_spec, arch_spec=arch_spec, scope=scope, use_cache=False
        )
        if compilers:
            scope_to_compilers[scope] = compilers

    cfg_file_to_duplicates = {}
    for scope, compilers in scope_to_compilers.items():
        config_file = config.get_config_filename(scope, "compilers")
        cfg_file_to_duplicates[config_file] = compilers

    return cfg_file_to_duplicates


@llnl.util.lang.memoized
def class_for_compiler_name(compiler_name):
    """Given a compiler module name, get the corresponding Compiler class."""
    if not supported(compiler_name):
        raise UnknownCompilerError(compiler_name)

    # Hack to be able to call the compiler `apple-clang` while still
    # using a valid python name for the module
    submodule_name = compiler_name
    if compiler_name == "apple-clang":
        submodule_name = compiler_name.replace("-", "_")

    module_name = ".".join(["spack", "compilers", submodule_name])
    module_obj = __import__(module_name, fromlist=[None])
    cls = getattr(module_obj, mod_to_class(compiler_name))

    # make a note of the name in the module so we can get to it easily.
    cls.name = compiler_name

    return cls


def all_os_classes():
    """
    Return the list of classes for all operating systems available on
    this platform
    """
    classes = []

    platform = spack.platforms.host()
    for os_class in platform.operating_sys.values():
        classes.append(os_class)

    return classes


def all_compiler_types():
    return [class_for_compiler_name(c) for c in supported_compilers()]


#: Gathers the attribute values by which a detected compiler is considered
#: unique in Spack.
#:
#:  - os: the operating system
#:  - compiler_name: the name of the compiler (e.g. 'gcc', 'clang', etc.)
#:  - version: the version of the compiler
#:
CompilerID = collections.namedtuple("CompilerID", ["os", "compiler_name", "version"])

#: Variations on a matched compiler name
NameVariation = collections.namedtuple("NameVariation", ["prefix", "suffix"])

#: Groups together the arguments needed by `detect_version`. The four entries
#: in the tuple are:
#:
#: - id: An instance of the CompilerID named tuple (version can be set to None
#:       as it will be detected later)
#: - variation: a NameVariation for file being tested
#: - language: compiler language being tested (one of 'cc', 'cxx', 'fc', 'f77')
#: - path: full path to the executable being tested
#:
DetectVersionArgs = collections.namedtuple(
    "DetectVersionArgs", ["id", "variation", "language", "path"]
)


def arguments_to_detect_version_fn(
    operating_system: spack.operating_systems.OperatingSystem, paths: List[str]
) -> List[DetectVersionArgs]:
    """Returns a list of DetectVersionArgs tuples to be used in a
    corresponding function to detect compiler versions.

    The ``operating_system`` instance can customize the behavior of this
    function by providing a method called with the same name.

    Args:
        operating_system: the operating system on which we are looking for compilers
        paths: paths to search for compilers

    Returns:
        List of DetectVersionArgs tuples. Each item in the list will be later
        mapped to the corresponding function call to detect the version of the
        compilers in this OS.
    """

    def _default(search_paths: List[str]) -> List[DetectVersionArgs]:
        command_arguments: List[DetectVersionArgs] = []
        files_to_be_tested = fs.files_in(*search_paths)
        for compiler_name in supported_compilers_for_host_platform():
            compiler_cls = class_for_compiler_name(compiler_name)

            for language in ("cc", "cxx", "f77", "fc"):
                # Select only the files matching a regexp
                for (file, full_path), regexp in itertools.product(
                    files_to_be_tested, compiler_cls.search_regexps(language)
                ):
                    match = regexp.match(file)
                    if match:
                        compiler_id = CompilerID(operating_system, compiler_name, None)
                        detect_version_args = DetectVersionArgs(
                            id=compiler_id,
                            variation=NameVariation(*match.groups()),
                            language=language,
                            path=full_path,
                        )
                        command_arguments.append(detect_version_args)

        return command_arguments

    fn = getattr(operating_system, "arguments_to_detect_version_fn", _default)
    return fn(paths)


def detect_version(
    detect_version_args: DetectVersionArgs,
) -> Tuple[Optional[DetectVersionArgs], Optional[str]]:
    """Computes the version of a compiler and adds it to the information
    passed as input.

    As this function is meant to be executed by worker processes it won't
    raise any exception but instead will return a (value, error) tuple that
    needs to be checked by the code dispatching the calls.

    Args:
        detect_version_args: information on the compiler for which we should detect the version.

    Returns:
        A ``(DetectVersionArgs, error)`` tuple. If ``error`` is ``None`` the
        version of the compiler was computed correctly and the first argument
        of the tuple will contain it. Otherwise ``error`` is a string
        containing an explanation on why the version couldn't be computed.
    """

    def _default(fn_args):
        compiler_id = fn_args.id
        language = fn_args.language
        compiler_cls = class_for_compiler_name(compiler_id.compiler_name)
        path = fn_args.path

        # Get compiler names and the callback to detect their versions
        callback = getattr(compiler_cls, f"{language}_version")

        try:
            version = callback(path)
            if version and str(version).strip() and version != "unknown":
                value = fn_args._replace(id=compiler_id._replace(version=version))
                return value, None

            error = f"Couldn't get version for compiler {path}".format(path)
        except spack.util.executable.ProcessError as e:
            error = f"Couldn't get version for compiler {path}\n" + str(e)
        except spack.util.executable.ProcessTimeoutError as e:
            error = f"Couldn't get version for compiler {path}\n" + str(e)
        except Exception as e:
            # Catching "Exception" here is fine because it just
            # means something went wrong running a candidate executable.
            error = "Error while executing candidate compiler {0}" "\n{1}: {2}".format(
                path, e.__class__.__name__, str(e)
            )
        return None, error

    operating_system = detect_version_args.id.os
    fn = getattr(operating_system, "detect_version", _default)
    return fn(detect_version_args)


def make_compiler_list(
    detected_versions: List[DetectVersionArgs], mixed_toolchain: bool = False
) -> List["spack.compiler.Compiler"]:
    """Process a list of detected versions and turn them into a list of
    compiler specs.

    Args:
        detected_versions: list of DetectVersionArgs containing a valid version
        mixed_toolchain: allow mixing compilers from different toolchains if langauge is missing

    Returns:
        list: list of Compiler objects
    """
    group_fn = lambda x: (x.id, x.variation, x.language)
    sorted_compilers = sorted(detected_versions, key=group_fn)

    # Gather items in a dictionary by the id, name variation and language
    compilers_d: Dict[CompilerID, Dict[NameVariation, dict]] = {}
    for sort_key, group in itertools.groupby(sorted_compilers, key=group_fn):
        compiler_id, name_variation, language = sort_key
        by_compiler_id = compilers_d.setdefault(compiler_id, {})
        by_name_variation = by_compiler_id.setdefault(name_variation, {})
        by_name_variation[language] = next(x.path for x in group)

    def _default_make_compilers(cmp_id, paths):
        operating_system, compiler_name, version = cmp_id
        compiler_cls = class_for_compiler_name(compiler_name)
        spec = spack.spec.CompilerSpec(compiler_cls.name, f"={version}")
        paths = [paths.get(x, None) for x in ("cc", "cxx", "f77", "fc")]
        # TODO: johnwparent - revist the following line as per discussion at:
        # https://github.com/spack/spack/pull/33385/files#r1040036318
        target = archspec.cpu.host()
        compiler = compiler_cls(spec, operating_system, str(target.family), paths)
        return [compiler]

    # For compilers with the same compiler id:
    #
    # - Prefer with C compiler to without
    # - Prefer with C++ compiler to without
    # - Prefer no variations to variations (e.g., clang to clang-gpu)
    #
    sort_fn = lambda variation: (
        "cc" not in by_compiler_id[variation],  # None last
        "cxx" not in by_compiler_id[variation],  # None last
        getattr(variation, "prefix", None),
        getattr(variation, "suffix", None),
    )

    # Flatten to a list of compiler id, primary variation and compiler dictionary
    flat_compilers: List[Tuple[CompilerID, NameVariation, dict]] = []
    for compiler_id, by_compiler_id in compilers_d.items():
        ordered = sorted(by_compiler_id, key=sort_fn)
        selected_variation = ordered[0]
        selected = by_compiler_id[selected_variation]

        # Fill any missing parts from subsequent entries (without mixing toolchains)
        for lang in ["cxx", "f77", "fc"]:
            if lang not in selected:
                next_lang = next(
                    (by_compiler_id[v][lang] for v in ordered if lang in by_compiler_id[v]), None
                )
                if next_lang:
                    selected[lang] = next_lang

        flat_compilers.append((compiler_id, selected_variation, selected))

    # Next, fill out the blanks of missing compilers by creating a mixed toolchain (if requested)
    if mixed_toolchain:
        make_mixed_toolchain(flat_compilers)

    # Finally, create the compiler list
    compilers = []
    for compiler_id, _, compiler in flat_compilers:
        make_compilers = getattr(compiler_id.os, "make_compilers", _default_make_compilers)
        compilers.extend(make_compilers(compiler_id, compiler))

    return compilers


def make_mixed_toolchain(compilers: List[Tuple[CompilerID, NameVariation, dict]]) -> None:
    """Add missing compilers across toolchains when they are missing for a particular language.
    This currently only adds the most sensible gfortran to (apple)-clang if it doesn't have a
    fortran compiler (no flang)."""

    # First collect the clangs that are missing a fortran compiler
    clangs_without_flang = [
        (id, variation, compiler)
        for id, variation, compiler in compilers
        if id.compiler_name in ("clang", "apple-clang")
        and "f77" not in compiler
        and "fc" not in compiler
    ]
    if not clangs_without_flang:
        return

    # Filter on GCCs with fortran compiler
    gccs_with_fortran = [
        (id, variation, compiler)
        for id, variation, compiler in compilers
        if id.compiler_name == "gcc" and "f77" in compiler and "fc" in compiler
    ]

    # Sort these GCCs by "best variation" (no prefix / suffix first)
    gccs_with_fortran.sort(
        key=lambda x: (getattr(x[1], "prefix", None), getattr(x[1], "suffix", None))
    )

    # Attach the optimal GCC fortran compiler to the clangs that don't have one
    for clang_id, _, clang_compiler in clangs_without_flang:
        gcc_compiler = next(
            (gcc[2] for gcc in gccs_with_fortran if gcc[0].os == clang_id.os), None
        )

        if not gcc_compiler:
            continue

        # Update the fc / f77 entries
        clang_compiler["f77"] = gcc_compiler["f77"]
        clang_compiler["fc"] = gcc_compiler["fc"]


def is_mixed_toolchain(compiler):
    """Returns True if the current compiler is a mixed toolchain,
    False otherwise.

    Args:
        compiler (spack.compiler.Compiler): a valid compiler object
    """
    cc = os.path.basename(compiler.cc or "")
    cxx = os.path.basename(compiler.cxx or "")
    f77 = os.path.basename(compiler.f77 or "")
    fc = os.path.basename(compiler.fc or "")

    toolchains = set()
    for compiler_cls in all_compiler_types():
        # Inspect all the compiler toolchain we know. If a compiler is the
        # only compiler supported there it belongs to that toolchain.
        def name_matches(name, name_list):
            # This is such that 'gcc' matches variations
            # like 'ggc-9' etc that are found in distros
            name, _, _ = name.partition("-")
            return len(name_list) == 1 and name and name in name_list

        if any(
            [
                name_matches(cc, compiler_cls.cc_names),
                name_matches(cxx, compiler_cls.cxx_names),
                name_matches(f77, compiler_cls.f77_names),
                name_matches(fc, compiler_cls.fc_names),
            ]
        ):
            tty.debug("[TOOLCHAIN] MATCH {0}".format(compiler_cls.__name__))
            toolchains.add(compiler_cls.__name__)

    if len(toolchains) > 1:
        if (
            toolchains == set(["Clang", "AppleClang", "Aocc"])
            # Msvc toolchain uses Intel ifx
            or toolchains == set(["Msvc", "Dpcpp", "Oneapi"])
        ):
            return False
        tty.debug("[TOOLCHAINS] {0}".format(toolchains))
        return True

    return False


class InvalidCompilerConfigurationError(spack.error.SpackError):
    def __init__(self, compiler_spec):
        super().__init__(
            'Invalid configuration for [compiler "%s"]: ' % compiler_spec,
            "Compiler configuration must contain entries for all compilers: %s"
            % _path_instance_vars,
        )


class NoCompilersError(spack.error.SpackError):
    def __init__(self):
        super().__init__("Spack could not find any compilers!")


class UnknownCompilerError(spack.error.SpackError):
    def __init__(self, compiler_name):
        super().__init__("Spack doesn't support the requested compiler: {0}".format(compiler_name))


class NoCompilerForSpecError(spack.error.SpackError):
    def __init__(self, compiler_spec, target):
        super().__init__(
            "No compilers for operating system %s satisfy spec %s" % (target, compiler_spec)
        )


class CompilerDuplicateError(spack.error.SpackError):
    def __init__(self, compiler_spec, arch_spec):
        config_file_to_duplicates = get_compiler_duplicates(compiler_spec, arch_spec)
        duplicate_table = list((x, len(y)) for x, y in config_file_to_duplicates.items())
        descriptor = lambda num: "time" if num == 1 else "times"
        duplicate_msg = lambda cfgfile, count: "{0}: {1} {2}".format(
            cfgfile, str(count), descriptor(count)
        )
        msg = (
            "Compiler configuration contains entries with duplicate"
            + " specification ({0}, {1})".format(compiler_spec, arch_spec)
            + " in the following files:\n\t"
            + "\n\t".join(duplicate_msg(x, y) for x, y in duplicate_table)
        )
        super().__init__(msg)


class CompilerSpecInsufficientlySpecificError(spack.error.SpackError):
    def __init__(self, compiler_spec):
        super().__init__("Multiple compilers satisfy spec %s" % compiler_spec)
