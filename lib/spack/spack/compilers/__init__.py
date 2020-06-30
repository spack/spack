# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module contains functions related to finding compilers on the
system and configuring Spack to use multiple compilers.
"""
import collections
import os

import llnl.util.lang
import llnl.util.tty as tty
import spack.architecture
import spack.config
import spack.detection.path
import spack.error
import spack.paths
import spack.repo
import spack.spec
import spack.util.imp as simp
from spack.util.naming import mod_to_class

_imported_compilers_module = 'spack.compilers'
_path_instance_vars = ['cc', 'cxx', 'f77', 'fc']
_flags_instance_vars = ['cflags', 'cppflags', 'cxxflags', 'fflags']
_other_instance_vars = ['modules', 'operating_system', 'environment',
                        'implicit_rpaths', 'extra_rpaths']
_cache_config_file = []

# TODO: Caches at module level make it difficult to mock configurations in
# TODO: unit tests. It might be worth reworking their implementation.
#: cache of compilers constructed from config data, keyed by config entry id.
_compiler_cache = {}

_compiler_to_pkg = {
    'clang': 'llvm+clang'
}

# TODO: list of packages that support current compilers. This needs
# TODO: to be removed when turning compilers to proper dependencies.
compiler_packages = [
    'apple-clang', 'arm', 'cce', 'fj', 'gcc', 'intel',
    'llvm', 'nag', 'pgi', 'xlc', 'xlf'
]


def pkg_spec_for_compiler(cspec):
    """Return the spec of the package that provides the compiler."""
    spec_str = '%s@%s' % (_compiler_to_pkg.get(cspec.name, cspec.name),
                          cspec.versions)
    return spack.spec.Spec(spec_str)


def _auto_compiler_spec(function):
    def converter(cspec_like, *args, **kwargs):
        if not isinstance(cspec_like, spack.spec.CompilerSpec):
            cspec_like = spack.spec.CompilerSpec(cspec_like)
        return function(cspec_like, *args, **kwargs)
    return converter


def _to_dict(compiler):
    """Return a dict version of compiler suitable to insert in YAML."""
    d = {}
    d['spec'] = str(compiler.spec)
    d['paths'] = dict((attr, getattr(compiler, attr, None))
                      for attr in _path_instance_vars)
    d['flags'] = dict((fname, fvals) for fname, fvals in compiler.flags)
    d['flags'].update(dict((attr, getattr(compiler, attr, None))
                      for attr in _flags_instance_vars
                           if hasattr(compiler, attr)))
    d['operating_system'] = str(compiler.operating_system)
    d['target'] = str(compiler.target)
    d['modules'] = compiler.modules or []
    d['environment'] = compiler.environment or {}
    d['extra_rpaths'] = compiler.extra_rpaths or []
    if compiler.enable_implicit_rpaths is not None:
        d['implicit_rpaths'] = compiler.enable_implicit_rpaths

    if compiler.alias:
        d['alias'] = compiler.alias

    return {'compiler': d}


def get_compiler_config(scope=None):
    """Return the compiler configuration for the specified architecture."""
    config = spack.config.get('compilers', scope=scope)
    # If there's no config, return an empty list which we will later append to
    if not config:
        return []
    return config


def compiler_config_files():
    config_files = list()
    config = spack.config.config
    for scope in config.file_scopes:
        name = scope.name
        compiler_config = config.get('compilers', scope=name)
        if compiler_config:
            config_files.append(config.get_config_filename(name, 'compilers'))
    return config_files


def add_compilers_to_config(compilers, scope=None):
    """Add compilers to the config for the specified architecture.

    Arguments:
      - compilers: a list of Compiler objects.
      - scope:     configuration scope to modify.
    """
    compiler_config = get_compiler_config(scope)
    for compiler in compilers:
        compiler_config.append(_to_dict(compiler))
    global _cache_config_file
    _cache_config_file = compiler_config
    spack.config.set('compilers', compiler_config, scope=scope)


@_auto_compiler_spec
def remove_compiler_from_config(compiler_spec, scope=None):
    """Remove compilers from the config, by spec.

    Arguments:
      - compiler_specs: a list of CompilerSpec objects.
      - scope:          configuration scope to modify.
    """
    # Need a better way for this
    global _cache_config_file

    compiler_config = get_compiler_config(scope)
    config_length = len(compiler_config)

    filtered_compiler_config = [
        comp for comp in compiler_config
        if spack.spec.CompilerSpec(comp['compiler']['spec']) != compiler_spec]

    # Update the cache for changes
    _cache_config_file = filtered_compiler_config
    if len(filtered_compiler_config) == config_length:  # No items removed
        CompilerSpecInsufficientlySpecificError(compiler_spec)
    spack.config.set('compilers', filtered_compiler_config, scope=scope)


def all_compilers_config(scope=None):
    """Return a set of specs for all the compiler versions currently
       available to build with.  These are instances of CompilerSpec.
    """
    # Get compilers for this architecture.
    # Create a cache of the config file so we don't load all the time.
    global _cache_config_file
    if not _cache_config_file:
        _cache_config_file = get_compiler_config(scope)
        return _cache_config_file
    else:
        return _cache_config_file


def all_compiler_specs(scope=None):
    # Return compiler specs from the merged config.
    return [spack.spec.CompilerSpec(s['compiler']['spec'])
            for s in all_compilers_config(scope)]


def supported_compilers():
    """Return a set of names of compilers supported by Spack.

       See available_compilers() to get a list of all the available
       versions of supported compilers.
    """
    # Hack to be able to call the compiler `apple-clang` while still
    # using a valid python name for the module
    return sorted(name if name != 'apple_clang' else 'apple-clang' for name in
                  llnl.util.lang.list_modules(spack.paths.compilers_path))


@_auto_compiler_spec
def supported(compiler_spec):
    """Test if a particular compiler is supported."""
    return compiler_spec.name in supported_compilers()


@_auto_compiler_spec
def find(compiler_spec, scope=None):
    """Return specs of available compilers that match the supplied
       compiler spec.  Return an empty list if nothing found."""
    return [c for c in all_compiler_specs(scope) if c.satisfies(compiler_spec)]


@_auto_compiler_spec
def find_specs_by_arch(compiler_spec, arch_spec, scope=None):
    """Return specs of available compilers that match the supplied
       compiler spec.  Return an empty list if nothing found."""
    return [c.spec for c in compilers_for_spec(
        compiler_spec, arch_spec, scope=scope, use_cache=True
    )]


def all_compilers(scope=None):
    config = get_compiler_config(scope)
    compilers = list()
    for items in config:
        items = items['compiler']
        compilers.append(_compiler_from_config_entry(items))
    return compilers


@_auto_compiler_spec
def compilers_for_spec(
        compiler_spec, arch_spec=None, scope=None, use_cache=True
):
    """This gets all compilers that satisfy the supplied CompilerSpec.
       Returns an empty list if none are found.
    """
    if use_cache:
        config = all_compilers_config(scope)
    else:
        config = get_compiler_config(scope)

    matches = set(find(compiler_spec, scope))
    compilers = []
    for cspec in matches:
        compilers.extend(get_compilers(config, cspec, arch_spec))
    return compilers


def compilers_for_arch(arch_spec, scope=None):
    config = all_compilers_config(scope)
    return list(get_compilers(config, arch_spec=arch_spec))


class CacheReference(object):
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
    cspec = spack.spec.CompilerSpec(items['spec'])
    os = items.get('operating_system', None)
    target = items.get('target', None)

    if not ('paths' in items and
            all(n in items['paths'] for n in _path_instance_vars)):
        raise InvalidCompilerConfigurationError(cspec)

    cls  = class_for_compiler_name(cspec.name)

    compiler_paths = []
    for c in _path_instance_vars:
        compiler_path = items['paths'][c]
        if compiler_path != 'None':
            compiler_paths.append(compiler_path)
        else:
            compiler_paths.append(None)

    mods = items.get('modules')
    if mods == 'None':
        mods = []

    alias = items.get('alias', None)
    compiler_flags = items.get('flags', {})
    environment = items.get('environment', {})
    extra_rpaths = items.get('extra_rpaths', [])
    implicit_rpaths = items.get('implicit_rpaths', None)

    # Starting with c22a145, 'implicit_rpaths' was a list. Now it is a
    # boolean which can be set by the user to disable all automatic
    # RPATH insertion of compiler libraries
    if implicit_rpaths is not None and not isinstance(implicit_rpaths, bool):
        implicit_rpaths = None

    return cls(cspec, os, target, compiler_paths, mods, alias,
               environment, extra_rpaths,
               enable_implicit_rpaths=implicit_rpaths,
               **compiler_flags)


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
        items = items['compiler']
        if cspec and items['spec'] != str(cspec):
            continue

        # If an arch spec is given, confirm that this compiler
        # is for the given operating system
        os = items.get('operating_system', None)
        if arch_spec and os != arch_spec.os:
            continue

        # If an arch spec is given, confirm that this compiler
        # is for the given target. If the target is 'any', match
        # any given arch spec. If the compiler has no assigned
        # target this is an old compiler config file, skip this logic.
        target = items.get('target', None)

        try:
            current_target = llnl.util.cpu.targets[str(arch_spec.target)]
            family = str(current_target.family)
        except KeyError:
            # TODO: Check if this exception handling makes sense, or if we
            # TODO: need to change / refactor tests
            family = arch_spec.target
        except AttributeError:
            assert arch_spec is None

        if arch_spec and target and (target != family and target != 'any'):
            # If the family of the target is the family we are seeking,
            # there's an error in the underlying configuration
            if llnl.util.cpu.targets[target].family == family:
                msg = ('the "target" field in compilers.yaml accepts only '
                       'target families [replace "{0}" with "{1}"'
                       ' in "{2}" specification]')
                msg = msg.format(str(target), family, items.get('spec', '??'))
                raise ValueError(msg)
            continue

        compilers.append(_compiler_from_config_entry(items))

    return compilers


@_auto_compiler_spec
def compiler_for_spec(compiler_spec, arch_spec):
    """Get the compiler that satisfies compiler_spec.  compiler_spec must
       be concrete."""
    assert(compiler_spec.concrete)
    assert(arch_spec.concrete)

    compilers = compilers_for_spec(compiler_spec, arch_spec=arch_spec)
    if len(compilers) < 1:
        raise NoCompilerForSpecError(compiler_spec, arch_spec.os)
    if len(compilers) > 1:
        msg = 'Multiple definitions of compiler %s' % compiler_spec
        msg += 'for architecture %s:\n %s' % (arch_spec, compilers)
        tty.debug(msg)
    return compilers[0]


@_auto_compiler_spec
def get_compiler_duplicates(compiler_spec, arch_spec):
    config = spack.config.config

    scope_to_compilers = {}
    for scope in config.scopes:
        compilers = compilers_for_spec(compiler_spec, arch_spec=arch_spec,
                                       scope=scope, use_cache=False)
        if compilers:
            scope_to_compilers[scope] = compilers

    cfg_file_to_duplicates = {}
    for scope, compilers in scope_to_compilers.items():
        config_file = config.get_config_filename(scope, 'compilers')
        cfg_file_to_duplicates[config_file] = compilers

    return cfg_file_to_duplicates


@llnl.util.lang.memoized
def class_for_compiler_name(compiler_name):
    """Given a compiler module name, get the corresponding Compiler class."""
    assert(supported(compiler_name))

    # Hack to be able to call the compiler `apple-clang` while still
    # using a valid python name for the module
    module_name = compiler_name
    if compiler_name == 'apple-clang':
        module_name = compiler_name.replace('-', '_')

    file_path = os.path.join(spack.paths.compilers_path, module_name + ".py")
    compiler_mod = simp.load_source(_imported_compilers_module, file_path)
    cls = getattr(compiler_mod, mod_to_class(compiler_name))

    # make a note of the name in the module so we can get to it easily.
    cls.name = compiler_name

    return cls


def all_os_classes():
    """
    Return the list of classes for all operating systems available on
    this platform
    """
    classes = []

    platform = spack.architecture.platform()
    for os_class in platform.operating_sys.values():
        classes.append(os_class)

    return classes


def all_compiler_types():
    return [class_for_compiler_name(c) for c in supported_compilers()]


def is_mixed_toolchain(compiler):
    """Returns True if the current compiler is a mixed toolchain,
    False otherwise.

    Args:
        compiler (Compiler): a valid compiler object
    """
    packages = []
    for package_name in compiler_packages:
        try:
            packages.append(spack.repo.get(package_name))
        except Exception:
            pass

    exes_by_pkg = spack.detection.path.executables_by_package(
        packages, {
            compiler.cc: os.path.basename(compiler.cc or ''),
            compiler.cxx: os.path.basename(compiler.cxx or ''),
            compiler.f77: os.path.basename(compiler.f77 or ''),
            compiler.fc: os.path.basename(compiler.fc or '')
        }
    )
    to_be_filtered = []
    for cls, exes in exes_by_pkg.items():
        filter_fn = getattr(cls, 'filter_detected_exes', lambda x, exes: exes)
        if not filter_fn(None, exes):
            to_be_filtered.append(cls)

    for cls in to_be_filtered:
        del exes_by_pkg[cls]

    toolchains = set(pkg.name for pkg in exes_by_pkg)
    if len(toolchains) > 1:
        # Apple's Clang and LLVM's Clang share the same names
        if toolchains == set(['llvm', 'apple-clang']):
            return False

        # Xl compilers have been split into two packages
        if toolchains == set(['xlc', 'xlf']):
            return False

        tty.debug("[MIXED COMPILER TOOLCHAIN] {0}".format(toolchains))
        return True

    return False


def _compilers_from(specs):
    partial_results = collections.defaultdict(list)
    for spec in specs:
        spec_to_compiler = {
            'llvm': 'clang',
            'xlc+r': 'xl_r', 'xlf+r': 'xl_r',
            'xlc~r': 'xl', 'xlf~r': 'xl',
        }
        compiler_name = spec.name
        for constraint, name in spec_to_compiler.items():
            if spec.satisfies(constraint):
                compiler_name = name
                break

        compiler_cls = spack.compilers.class_for_compiler_name(compiler_name)
        cspec = spack.spec.CompilerSpec(compiler_cls.name, spec.version)
        paths = [
            getattr(spec.package, 'cc', None),
            getattr(spec.package, 'cxx', None),
            getattr(spec.package, 'fortran', None),
            getattr(spec.package, 'fortran', None)
        ]
        if not spec.concrete:
            c = spack.concretize.Concretizer(str(spec))
            c.concretize_architecture(spec)

        # For external packages detected on Cray the OS is annotated
        spec_os = spec.os
        if spec.extra_attributes and 'cray' in spec.extra_attributes:
            spec_os = spec.extra_attributes['cray']['os']

        partial_results[(cspec, spec_os)].append(compiler_cls(
            cspec, spec_os, str(spec.target.family), paths,
            modules=spec.external_modules
        ))

    # Merge multiple matches over the same compiler spec and OS
    result = []
    for (cspec, spec_os), compilers in partial_results.items():
        candidate = compilers[0]
        for item in compilers[1:]:
            candidate.cc = candidate.cc or item.cc
            candidate.cxx = candidate.cxx or item.cxx
            candidate.f77 = candidate.f77 or item.f77
            candidate.fc = candidate.fc or item.fc
        result.append(candidate)

    return result


def from_externals():
    """Return a list of compilers listed as externals in packages.yaml"""
    externals = []
    for current_compiler in compiler_packages:
        externals.extend(spack.package_prefs.spec_externals(
            spack.spec.Spec(current_compiler)
        ))
    return _compilers_from(externals)


def from_db():
    """Return a list of compilers installed in Spack's store"""
    compilers = []
    for current_compiler in compiler_packages:
        specs = spack.store.db.query(current_compiler)
        compilers.extend(_compilers_from(specs))
    return compilers


def not_registered(compilers):
    """Given a list of compilers, return the ones that are not
    available to Spack yet.

    Args:
        compilers (list): list of candidate compilers

    Returns:
        Compilers in the list that are not available to Spack yet
    """
    new_compilers = []
    for current_compiler in compilers:
        arch_spec = spack.spec.ArchSpec(
            (None, current_compiler.operating_system, current_compiler.target)
        )
        same_specs = spack.compilers.compilers_for_spec(
            current_compiler.spec, arch_spec
        )

        if not same_specs:
            new_compilers.append(current_compiler)
    return new_compilers


class InvalidCompilerConfigurationError(spack.error.SpackError):

    def __init__(self, compiler_spec):
        super(InvalidCompilerConfigurationError, self).__init__(
            "Invalid configuration for [compiler \"%s\"]: " % compiler_spec,
            "Compiler configuration must contain entries for all compilers: %s"
            % _path_instance_vars)


class NoCompilersError(spack.error.SpackError):
    def __init__(self):
        super(NoCompilersError, self).__init__(
            "Spack could not find any compilers!")


class NoCompilerForSpecError(spack.error.SpackError):
    def __init__(self, compiler_spec, target):
        super(NoCompilerForSpecError, self).__init__(
            "No compilers for operating system %s satisfy spec %s"
            % (target, compiler_spec))


class CompilerDuplicateError(spack.error.SpackError):
    def __init__(self, compiler_spec, arch_spec):
        config_file_to_duplicates = get_compiler_duplicates(
            compiler_spec, arch_spec)
        duplicate_table = list(
            (x, len(y)) for x, y in config_file_to_duplicates.items())
        descriptor = lambda num: 'time' if num == 1 else 'times'
        duplicate_msg = (
            lambda cfgfile, count: "{0}: {1} {2}".format(
                cfgfile, str(count), descriptor(count)))
        msg = (
            "Compiler configuration contains entries with duplicate" +
            " specification ({0}, {1})".format(compiler_spec, arch_spec) +
            " in the following files:\n\t" +
            '\n\t'.join(duplicate_msg(x, y) for x, y in duplicate_table))
        super(CompilerDuplicateError, self).__init__(msg)


class CompilerSpecInsufficientlySpecificError(spack.error.SpackError):
    def __init__(self, compiler_spec):
        super(CompilerSpecInsufficientlySpecificError, self).__init__(
            "Multiple compilers satisfy spec %s" % compiler_spec)
