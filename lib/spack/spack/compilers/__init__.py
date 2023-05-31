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
from typing import Any, Dict, List, Optional, Tuple, Type, Union

import archspec.cpu

import llnl.util.filesystem as fs
import llnl.util.lang
import llnl.util.tty as tty

import spack.compiler
import spack.config
import spack.error
import spack.paths
import spack.platforms
import spack.spec
import spack.version
from spack.util.environment import get_path
from spack.util.naming import mod_to_class

_PATH_INSTANCE_VARS = ["cc", "cxx", "f77", "fc"]

#: cache of compilers constructed from config data, keyed by config entry id.
CACHE: Dict["CacheReference", "spack.compiler.Compiler"] = {}


#: Maps package names in Spack to the compiler name they provide
PACKAGE_TO_COMPILER = {
    "llvm": "clang",
    "intel-oneapi-compilers": "oneapi",
    "llvm-amdgpu": "rocmcc",
    "intel-oneapi-compilers-classic": "intel",
    "acfl": "arm",
}


class CompilerQuery:
    def __init__(self, compiler_query: Union[str, spack.spec.CompilerSpec]) -> None:
        if not isinstance(compiler_query, spack.spec.CompilerSpec):
            compiler_query = spack.spec.CompilerSpec(compiler_query)
        self.compiler_spec: spack.spec.CompilerSpec = compiler_query

    def supported(self) -> bool:
        """Returns True if the compiler is currently supported by Spack, False otherwise."""
        return self.compiler_spec.name in supported_compilers()

    def ensure_one(self, *, arch_spec: spack.spec.ArchSpec) -> spack.compiler.Compiler:
        """Ensures that there is at least one compiler in the configuration matching the query,
        and returns the first match.

        Args:
            arch_spec: architecture targeted by the compiler

        Raises:
            NoCompilerForSpecError: if there is no matching compiler
        """
        assert self.compiler_spec.concrete
        assert arch_spec.concrete

        compilers = self.all_compilers(arch_spec=arch_spec)

        if len(compilers) < 1:
            raise NoCompilerForSpecError(self.compiler_spec, arch_spec.os)

        if len(compilers) > 1:
            msg = (
                f"Multiple definitions of '{self.compiler_spec}' for architecture"
                f" {arch_spec}:\n {compilers}"
            )
            tty.debug(msg)

        return compilers[0]

    def all_compilers(
        self,
        *,
        arch_spec: Optional[spack.spec.ArchSpec] = None,
        scope: Optional[str] = None,
        init_config: bool = True,
    ) -> List[spack.compiler.Compiler]:
        """Returns all the compilers that satisfy the query and arguments.

        Args:
            arch_spec: architecture targeted by the compiler
            scope: configuration scope to look into
            init_config: if True, initialize the configuration  when no
                compiler is available
        """
        cfg = compiler_config(scope=scope, init_config=init_config)
        matches = set(self.all_specs(scope=scope, init_config=init_config))
        compilers = []
        for current_compiler in matches:
            compilers.extend(get_compilers(cfg, current_compiler, arch_spec))
        return compilers

    def all_specs(
        self,
        *,
        arch_spec: Optional[spack.spec.ArchSpec] = None,
        scope: Optional[str] = None,
        init_config: bool = True,
    ) -> List[spack.spec.CompilerSpec]:
        """Returns all the compiler specs that satisfy the query and arguments.

        Args:
            arch_spec: architecture targeted by the compiler
            scope: configuration scope to look into
            init_config: if True, initialize the configuration  when no
                compiler is available
        """
        return [
            c
            for c in all_compiler_specs(arch_spec=arch_spec, scope=scope, init_config=init_config)
            if c.satisfies(self.compiler_spec)
        ]


def pkg_spec_for_compiler(compiler_spec: spack.spec.CompilerSpec) -> spack.spec.Spec:
    """Returns the spec of the package that provides the compiler spec passed as input."""
    compiler_to_package = {
        "clang": "llvm+clang",
        "oneapi": "intel-oneapi-compilers",
        "rocmcc": "llvm-amdgpu",
        "intel@2020:": "intel-oneapi-compilers-classic",
        "arm": "acfl",
    }
    for compiler_constraint, package in compiler_to_package.items():
        if compiler_spec.satisfies(compiler_constraint):
            spec_str = f"{package}@{compiler_spec.versions}"
            break
    else:
        spec_str = str(compiler_spec)
    return spack.spec.parse_with_version_concrete(spec_str)


def _to_dict(compiler: spack.compiler.Compiler) -> Any:
    """Return a dict version of compiler suitable to insert in YAML."""
    flags = {fname: " ".join(fvals) for fname, fvals in compiler.flags.items()}
    flags.update(
        {
            attr: getattr(compiler, attr, None)
            for attr in spack.spec.FlagMap.valid_compiler_flags()
            if hasattr(compiler, attr)
        }
    )
    d = {
        "spec": str(compiler.spec),
        "paths": {attr: getattr(compiler, attr, None) for attr in _PATH_INSTANCE_VARS},
        "flags": flags,
        "operating_system": str(compiler.operating_system),
        "target": str(compiler.target),
        "modules": compiler.modules or [],
        "environment": compiler.environment or {},
        "extra_rpaths": compiler.extra_rpaths or [],
    }

    if compiler.enable_implicit_rpaths is not None:
        d["implicit_rpaths"] = compiler.enable_implicit_rpaths

    if compiler.alias:
        d["alias"] = compiler.alias

    return {"compiler": d}


def compiler_config(*, scope: Optional[str] = None, init_config: bool = True) -> Any:
    """Returns the compiler configuration for a given scope.

    If scope is None, the merged configuration is returned.

    Args:
        scope: configuration scope to get
        init_config: if True, initialize configuration files if no compilers are available
    """
    config = spack.config.get("compilers", scope=scope) or []
    if config or not init_config:
        return config

    merged_config = spack.config.get("compilers")
    if merged_config:
        return config

    _init_compiler_config(scope=scope)
    config = spack.config.get("compilers", scope=scope)
    return config


def _init_compiler_config(*, scope: Optional[str]) -> None:
    """Compiler search used when Spack has no compilers."""
    compilers = find_compilers()
    compilers_dict = []
    for compiler in compilers:
        compilers_dict.append(_to_dict(compiler))
    spack.config.set("compilers", compilers_dict, scope=scope)


def add_compilers_to_config(
    compilers: List[spack.compiler.Compiler],
    *,
    scope: Optional[str] = None,
    init_config: bool = True,
) -> None:
    """Add the compilers passed as arguments to the configuration.

    Arguments:
        compilers: compilers to be added
        scope: configuration scope to modify
        init_config: if True, initialize configuration files if no compilers are available
    """
    compiler_cfg = compiler_config(scope=scope, init_config=init_config)
    for compiler in compilers:
        compiler_cfg.append(_to_dict(compiler))
    spack.config.set("compilers", compiler_cfg, scope=scope)


def remove_compiler_from_config(
    compiler_spec: Union[str, spack.spec.CompilerSpec], *, scope: Optional[str] = None
) -> bool:
    """Remove compilers from configuration by spec.

    If scope is None, all the scopes are searched for removal.

    Args:
        compiler_spec: compiler to be removed
        scope: configuration scope to modify

    Returns:
        True if any compiler has been removed, False otherwise
    """
    if not isinstance(compiler_spec, spack.spec.CompilerSpec):
        compiler_spec = spack.spec.CompilerSpec(compiler_spec)

    candidate_scopes = [scope]
    if scope is None:
        candidate_scopes = list(spack.config.config.scopes.keys())

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
    compiler_cfg = compiler_config(scope=scope)
    filtered_compiler_config = [
        compiler_entry
        for compiler_entry in compiler_cfg
        if not spack.spec.parse_with_version_concrete(
            compiler_entry["compiler"]["spec"], compiler=True
        ).satisfies(compiler_spec)
    ]

    if len(filtered_compiler_config) == len(compiler_cfg):
        return False

    # We need to preserve the YAML type for comments, hence we are copying the
    # items in the list that has just been retrieved
    compiler_cfg[:] = filtered_compiler_config
    spack.config.set("compilers", compiler_cfg, scope=scope)
    return True


def all_compiler_specs(
    *,
    arch_spec: Optional[spack.spec.ArchSpec] = None,
    scope: Optional[str] = None,
    init_config: bool = True,
) -> List[spack.spec.CompilerSpec]:
    """Returns the list of compiler specs matching the argument passed as input.

    Args:
        arch_spec: architecture targeted by the compiler
        scope: configuration scope to look into
        init_config: if True, initialize the configuration when no compiler is available
    """
    config_entries = compiler_config(scope=scope, init_config=init_config)
    return [
        spack.spec.parse_with_version_concrete(s["compiler"]["spec"], compiler=True)
        for s in filter_configuration_entries(config_entries, arch_spec=arch_spec)
    ]


def find_compilers(path_hints: Optional[List[str]] = None) -> List[spack.compiler.Compiler]:
    """Returns the list of compilers found in the paths given as arguments.

    Args:
        path_hints: list of path hints where to look for. If None, use defaults extracted from the
            ``PATH`` environment variable
    """
    if path_hints is None:
        path_hints = get_path("PATH")
    default_paths = fs.search_paths_for_executables(*path_hints)

    # To detect the version of the compilers, we dispatch a certain number
    # of function calls to different workers. Here we construct the list
    # of arguments for each call.
    arguments = []
    for o in _all_os_classes():
        search_paths = getattr(o, "compiler_search_paths", default_paths)
        arguments.extend(arguments_to_detect_version_fn(o, search_paths))

    # Here we map the function arguments to the corresponding calls
    tp = multiprocessing.pool.ThreadPool()
    try:
        detected_versions = tp.map(detect_version, arguments)
    finally:
        tp.close()

    def valid_version(item):
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

    def remove_errors(item):
        value, _ = item
        return value

    filtered_version_list = list(map(remove_errors, filter(valid_version, detected_versions)))
    return make_compiler_list(filtered_version_list)


def find_new_compilers(
    path_hints: Optional[List[str]] = None, scope: Optional[str] = None
) -> List[spack.compiler.Compiler]:
    """Same as ``find_compilers`` but return only the compilers that are not
    already in compilers.yaml.

    Args:
        path_hints: list of path hints where to look for. If None, use defaults extracted from the
            ``PATH`` environment variable
        scope: scope to look for a compiler. If None, consider the merged configuration
    """
    compilers = find_compilers(path_hints)
    return select_new_compilers(compilers, scope)


def select_new_compilers(
    compilers: List[spack.compiler.Compiler], scope: Optional[str] = None
) -> List[spack.compiler.Compiler]:
    """Given a list of compilers, returns the one that are not already defined in
    the configuration.

    Args:
        compilers: list of compilers to be considered
        scope: scope to look for a compiler. If None, consider the merged configuration
    """
    compilers_not_in_config = []
    for c in compilers:
        arch_spec = spack.spec.ArchSpec((None, c.operating_system, c.target))
        same_specs = CompilerQuery(c.spec).all_compilers(
            arch_spec=arch_spec, scope=scope, init_config=False
        )
        if not same_specs:
            compilers_not_in_config.append(c)

    return compilers_not_in_config


def supported_compilers() -> List[str]:
    """List of compiler names supported by Spack."""
    # Hack to be able to call the compiler `apple-clang` while still
    # using a valid python name for the module
    return sorted(
        name if name != "apple_clang" else "apple-clang"
        for name in llnl.util.lang.list_modules(spack.paths.compilers_path)
    )


def all_compilers(
    scope: Optional[str] = None, init_config: bool = True
) -> List[spack.compiler.Compiler]:
    """Returns all the compilers matching the arguments.

    Args:
        scope: configuration scope to look into
        init_config: if True, initialize the configuration when no compiler is available
    """
    config = compiler_config(scope=scope, init_config=init_config)
    compilers = list()
    for items in config:
        items = items["compiler"]
        compilers.append(_compiler_from_config_entry(items))
    return compilers


def compilers_for_arch(
    arch_spec: spack.spec.ArchSpec, scope: Optional[str] = None
) -> List[spack.compiler.Compiler]:
    config = compiler_config(scope=scope, init_config=True)
    return list(get_compilers(config, arch_spec=arch_spec))


def compiler_specs_for_arch(
    arch_spec: spack.spec.ArchSpec, scope: Optional[str] = None
) -> List[spack.spec.CompilerSpec]:
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

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, CacheReference) and self.id == other.id


def compiler_from_dict(items: Any) -> spack.compiler.Compiler:
    cspec = spack.spec.parse_with_version_concrete(items["spec"], compiler=True)
    os = items.get("operating_system", None)
    target = items.get("target", None)

    if not ("paths" in items and all(n in items["paths"] for n in _PATH_INSTANCE_VARS)):
        raise InvalidCompilerConfigurationError(cspec)

    cls = class_for_compiler_name(cspec.name)

    compiler_paths = []
    for c in _PATH_INSTANCE_VARS:
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


def _compiler_from_config_entry(items: Any) -> spack.compiler.Compiler:
    """Note this is intended for internal use only. To avoid re-parsing
    the same config dictionary this keeps track of its location in
    memory. If you provide the same dictionary twice it will return
    the same Compiler object (regardless of whether the dictionary
    entries have changed).
    """
    config_id = CacheReference(items)
    compiler = CACHE.get(config_id, None)

    if compiler is None:
        compiler = compiler_from_dict(items)
        CACHE[config_id] = compiler

    return compiler


def filter_configuration_entries(
    config: List[Any],
    cspec: Optional[spack.spec.CompilerSpec] = None,
    arch_spec: Optional[spack.spec.ArchSpec] = None,
) -> List[Any]:
    result = []
    for entry in config:
        compiler_entry = entry["compiler"]

        # NOTE: in principle this should be equality not satisfies, but config can still
        # be written in old format gcc@10.1.0 instead of gcc@=10.1.0.
        if cspec and not cspec.satisfies(compiler_entry["spec"]):
            continue

        # If an arch spec is given, confirm that this compiler
        # is for the given operating system
        os = compiler_entry.get("operating_system", None)
        if arch_spec and os != arch_spec.os:
            continue

        # If an arch spec is given, confirm that this compiler
        # is for the given target. If the target is 'any', match
        # any given arch spec. If the compiler has no assigned
        # target this is an old compiler config file, skip this logic.
        target = compiler_entry.get("target", None)

        if arch_spec is not None:
            try:
                current_target = archspec.cpu.TARGETS[str(arch_spec.target)]
                family = str(current_target.family)
            except KeyError:
                # TODO: Check if this exception handling makes sense, or if we
                # TODO: need to change / refactor tests
                family = arch_spec.target

        if arch_spec and target and (target != family and target != "any"):
            # If the family of the target is the family we are seeking,
            # there's an error in the underlying configuration
            if archspec.cpu.TARGETS[target].family == family:
                msg = (
                    'the "target" field in compilers.yaml accepts only '
                    'target families [replace "{0}" with "{1}"'
                    ' in "{2}" specification]'
                )
                msg = msg.format(str(target), family, compiler_entry.get("spec", "??"))
                raise ValueError(msg)
            continue

        result.append(entry)

    return result


def get_compilers(
    config: Any,
    cspec: Optional[spack.spec.CompilerSpec] = None,
    arch_spec: Optional[spack.spec.ArchSpec] = None,
) -> List[spack.compiler.Compiler]:
    candidate_entries = filter_configuration_entries(config, cspec=cspec, arch_spec=arch_spec)
    return [_compiler_from_config_entry(x["compiler"]) for x in candidate_entries]


def get_compiler_duplicates(
    compiler_spec: spack.spec.CompilerSpec, arch_spec: spack.spec.ArchSpec
) -> Dict[str, List[spack.compiler.Compiler]]:
    config = spack.config.config

    scope_to_compilers = {}
    for scope in config.scopes:
        compilers = CompilerQuery(compiler_spec).all_compilers(
            arch_spec=arch_spec, scope=scope, init_config=True
        )
        if compilers:
            scope_to_compilers[scope] = compilers

    cfg_file_to_duplicates = {}
    for scope, compilers in scope_to_compilers.items():
        config_file = config.get_config_filename(scope, "compilers")
        cfg_file_to_duplicates[config_file] = compilers

    return cfg_file_to_duplicates


@llnl.util.lang.memoized
def class_for_compiler_name(compiler_name: str) -> Type[spack.compiler.Compiler]:
    """Given a compiler module name, get the corresponding Compiler class."""
    if not CompilerQuery(compiler_name).supported():
        raise UnknownCompilerError(compiler_name)

    # Hack to be able to call the compiler `apple-clang` while still
    # using a valid python name for the module
    submodule_name = compiler_name
    if compiler_name == "apple-clang":
        submodule_name = compiler_name.replace("-", "_")

    module_name = ".".join(["spack", "compilers", submodule_name])
    module_obj = __import__(module_name, fromlist=[""])
    cls = getattr(module_obj, mod_to_class(compiler_name))

    # make a note of the name in the module so we can get to it easily.
    cls.name = compiler_name

    return cls


def _all_os_classes():
    """Return the list of classes for all operating systems available on
    this platform
    """
    classes = []

    platform = spack.platforms.host()
    for os_class in platform.operating_sys.values():
        classes.append(os_class)

    return classes


def all_compiler_types() -> List[Type[spack.compiler.Compiler]]:
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

    def _default(search_paths):
        command_arguments = []
        files_to_be_tested = fs.files_in(*search_paths)
        for compiler_name in spack.compilers.supported_compilers():
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
) -> Tuple[DetectVersionArgs, Optional[str]]:
    """Computes the version of a compiler and adds it to the information
    passed as input.

    As this function is meant to be executed by worker processes it won't
    raise any exception but instead will return a (value, error) tuple that
    needs to be checked by the code dispatching the calls.

    Args:
        detect_version_args (DetectVersionArgs): information on the
            compiler for which we should detect the version.

    Returns:
        A ``(DetectVersionArgs, error)`` tuple. If ``error`` is ``None`` the
        version of the compiler was computed correctly and the first argument
        of the tuple will contain it. Otherwise, ``error`` is a string
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

            error = f"Couldn't get version for compiler {path}"
        except spack.util.executable.ProcessError as e:
            error = f"Couldn't get version for compiler {path}\n" + str(e)
        except Exception as e:
            # Catching "Exception" here is fine because it just
            # means something went wrong running a candidate executable.
            error = "Error while executing candidate compiler {}" "\n{}: {}".format(
                path, e.__class__.__name__, str(e)
            )
        return None, error

    operating_system = detect_version_args.id.os
    fn = getattr(operating_system, "detect_version", _default)
    return fn(detect_version_args)


def make_compiler_list(
    detected_versions: List[DetectVersionArgs],
) -> List[spack.compiler.Compiler]:
    """Process a list of detected versions and turn them into a list of
    compiler specs.

    Args:
        detected_versions: list of DetectVersionArgs containing a valid version

    Returns:
        list: list of Compiler objects
    """
    group_fn = lambda x: (x.id, x.variation, x.language)
    sorted_compilers = sorted(detected_versions, key=group_fn)

    # Gather items in a dictionary by the id, name variation and language
    compilers_d: Dict[Any, Any] = {}
    for sort_key, group in itertools.groupby(sorted_compilers, key=group_fn):
        compiler_id, name_variation, language = sort_key
        by_compiler_id = compilers_d.setdefault(compiler_id, {})
        by_name_variation = by_compiler_id.setdefault(name_variation, {})
        by_name_variation[language] = next(x.path for x in group)

    def _default_make_compilers(cmp_id, paths):
        operating_system, compiler_name, version = cmp_id
        compiler_cls = spack.compilers.class_for_compiler_name(compiler_name)
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

    compilers = []
    for compiler_id, by_compiler_id in compilers_d.items():
        ordered = sorted(by_compiler_id, key=sort_fn)
        selected_variation = ordered[0]
        selected = by_compiler_id[selected_variation]

        # fill any missing parts from subsequent entries
        for lang in ["cxx", "f77", "fc"]:
            if lang not in selected:
                next_lang = next(
                    (by_compiler_id[v][lang] for v in ordered if lang in by_compiler_id[v]), None
                )
                if next_lang:
                    selected[lang] = next_lang

        operating_system, _, _ = compiler_id
        make_compilers = getattr(operating_system, "make_compilers", _default_make_compilers)

        compilers.extend(make_compilers(compiler_id, selected))

    return compilers


def is_mixed_toolchain(compiler: spack.compiler.Compiler) -> bool:
    """Returns True if the current compiler is a mixed toolchain,
    False otherwise.

    Args:
        compiler: a valid compiler object
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
            tty.debug(f"[TOOLCHAIN] MATCH {compiler_cls.__name__}")
            toolchains.add(compiler_cls.__name__)

    if len(toolchains) > 1:
        if (
            toolchains == {"Clang", "AppleClang", "Aocc"}
            # Msvc toolchain uses Intel ifx
            or toolchains == {"Msvc", "Dpcpp", "Oneapi"}
        ):
            return False
        tty.debug(f"[TOOLCHAINS] {toolchains}")
        return True

    return False


class InvalidCompilerConfigurationError(spack.error.SpackError):
    def __init__(self, compiler_spec):
        super().__init__(
            f'Invalid configuration for [compiler "{compiler_spec}"]: ',
            f"Compiler configuration must contain the following entries: {_PATH_INSTANCE_VARS}",
        )


class NoCompilersError(spack.error.SpackError):
    def __init__(self):
        super().__init__("Spack could not find any compilers!")


class UnknownCompilerError(spack.error.SpackError):
    def __init__(self, compiler_name):
        super().__init__(f"Spack doesn't support the requested compiler: {compiler_name}")


class NoCompilerForSpecError(spack.error.SpackError):
    def __init__(self, compiler_spec, target):
        super().__init__(
            f"No compilers for operating system {target} satisfy spec {compiler_spec}"
        )


class CompilerDuplicateError(spack.error.SpackError):
    def __init__(self, compiler_spec, arch_spec):
        config_file_to_duplicates = get_compiler_duplicates(compiler_spec, arch_spec)
        duplicate_table = list((x, len(y)) for x, y in config_file_to_duplicates.items())
        descriptor = lambda num: "time" if num == 1 else "times"
        duplicate_msg = lambda cfgfile, count: "{}: {} {}".format(
            cfgfile, str(count), descriptor(count)
        )
        msg = (
            "Compiler configuration contains entries with duplicate"
            + f" specification ({compiler_spec}, {arch_spec})"
            + " in the following files:\n\t"
            + "\n\t".join(duplicate_msg(x, y) for x, y in duplicate_table)
        )
        super().__init__(msg)


class CompilerSpecInsufficientlySpecificError(spack.error.SpackError):
    def __init__(self, compiler_spec):
        super().__init__(f"Multiple compilers satisfy spec {compiler_spec}")
