##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""This module contains functions related to finding compilers on the
system and configuring Spack to use multiple compilers.
"""
import imp

from llnl.util.lang import list_modules
from llnl.util.filesystem import join_path

import spack
import spack.error
import spack.spec
import spack.config
import spack.architecture

from spack.util.naming import mod_to_class

_imported_compilers_module = 'spack.compilers'
_path_instance_vars = ['cc', 'cxx', 'f77', 'fc']
_flags_instance_vars = ['cflags', 'cppflags', 'cxxflags', 'fflags']
_other_instance_vars = ['modules', 'operating_system', 'environment',
                        'extra_rpaths']
_cache_config_file = []


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
    d['modules'] = compiler.modules if compiler.modules else []
    d['environment'] = compiler.environment if compiler.environment else {}
    d['extra_rpaths'] = compiler.extra_rpaths if compiler.extra_rpaths else []

    if compiler.alias:
        d['alias'] = compiler.alias

    return {'compiler': d}


def get_compiler_config(scope=None, init_config=True):
    """Return the compiler configuration for the specified architecture.
    """
    def init_compiler_config():
        """Compiler search used when Spack has no compilers."""
        compilers = find_compilers()
        compilers_dict = []
        for compiler in compilers:
            compilers_dict.append(_to_dict(compiler))
        spack.config.update_config('compilers', compilers_dict, scope=scope)

    config = spack.config.get_config('compilers', scope=scope)
    # Update the configuration if there are currently no compilers
    # configured.  Avoid updating automatically if there ARE site
    # compilers configured but no user ones.
    if not config and init_config:
        if scope is None:
            # We know no compilers were configured in any scope.
            init_compiler_config()
            config = spack.config.get_config('compilers', scope=scope)
        elif scope == 'user':
            # Check the site config and update the user config if
            # nothing is configured at the site level.
            site_config = spack.config.get_config('compilers', scope='site')
            if not site_config:
                init_compiler_config()
                config = spack.config.get_config('compilers', scope=scope)
        return config
    elif config:
        return config
    else:
        return []  # Return empty list which we will later append to.


def compiler_config_files():
    config_files = list()
    for scope in spack.config.config_scopes:
        config = spack.config.get_config('compilers', scope=scope)
        if config:
            config_files.append(spack.config.config_scopes[scope]
                                .get_section_filename('compilers'))
    return config_files


def add_compilers_to_config(compilers, scope=None, init_config=True):
    """Add compilers to the config for the specified architecture.

    Arguments:
      - compilers: a list of Compiler objects.
      - scope:     configuration scope to modify.
    """
    compiler_config = get_compiler_config(scope, init_config)
    for compiler in compilers:
        compiler_config.append(_to_dict(compiler))
    global _cache_config_file
    _cache_config_file = compiler_config
    spack.config.update_config('compilers', compiler_config, scope)


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
    spack.config.update_config('compilers', filtered_compiler_config, scope)


def all_compilers_config(scope=None, init_config=True):
    """Return a set of specs for all the compiler versions currently
       available to build with.  These are instances of CompilerSpec.
    """
    # Get compilers for this architecture.
    # Create a cache of the config file so we don't load all the time.
    global _cache_config_file
    if not _cache_config_file:
        _cache_config_file = get_compiler_config(scope, init_config)
        return _cache_config_file
    else:
        return _cache_config_file


def all_compiler_specs(scope=None, init_config=True):
    # Return compiler specs from the merged config.
    return [spack.spec.CompilerSpec(s['compiler']['spec'])
            for s in all_compilers_config(scope, init_config)]


def find_compilers(*paths):
    """Return a list of compilers found in the suppied paths.
       This invokes the find_compilers() method for each operating
       system associated with the host platform, and appends
       the compilers detected to a list.
    """
    # Find compilers for each operating system class
    oss = all_os_classes()
    compiler_lists = []
    for o in oss:
        compiler_lists.extend(o.find_compilers(*paths))
    return compiler_lists


def supported_compilers():
    """Return a set of names of compilers supported by Spack.

       See available_compilers() to get a list of all the available
       versions of supported compilers.
    """
    return sorted(name for name in list_modules(spack.compilers_path))


@_auto_compiler_spec
def supported(compiler_spec):
    """Test if a particular compiler is supported."""
    return compiler_spec.name in supported_compilers()


@_auto_compiler_spec
def find(compiler_spec, scope=None, init_config=True):
    """Return specs of available compilers that match the supplied
       compiler spec.  Return an empty list if nothing found."""
    return [c for c in all_compiler_specs(scope, init_config)
            if c.satisfies(compiler_spec)]


def all_compilers(scope=None):
    config = get_compiler_config(scope)
    compilers = list()
    for items in config:
        items = items['compiler']
        compilers.append(compiler_from_config_entry(items))
    return compilers


@_auto_compiler_spec
def compilers_for_spec(compiler_spec, arch_spec=None, scope=None,
                       use_cache=True, init_config=True):
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


def compiler_from_config_entry(items):
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

    return cls(cspec, os, target, compiler_paths, mods, alias,
               environment, extra_rpaths, **compiler_flags)


def get_compilers(config, cspec=None, arch_spec=None):
    compilers = []

    for items in config:
        items = items['compiler']
        if cspec and items['spec'] != str(cspec):
            continue

        # If an arch spec is given, confirm that this compiler
        # is for the given operating system
        os = items.get('operating_system', None)
        if arch_spec and os != arch_spec.platform_os:
            continue

        # If an arch spec is given, confirm that this compiler
        # is for the given target. If the target is 'any', match
        # any given arch spec. If the compiler has no assigned
        # target this is an old compiler config file, skip this logic.
        target = items.get('target', None)
        if arch_spec and target and (target != arch_spec.target and
                                     target != 'any'):
            continue

        compilers.append(compiler_from_config_entry(items))

    return compilers


@_auto_compiler_spec
def compiler_for_spec(compiler_spec, arch_spec):
    """Get the compiler that satisfies compiler_spec.  compiler_spec must
       be concrete."""
    assert(compiler_spec.concrete)
    assert(arch_spec.concrete)

    compilers = compilers_for_spec(compiler_spec, arch_spec=arch_spec)
    if len(compilers) < 1:
        raise NoCompilerForSpecError(compiler_spec, arch_spec.platform_os)
    if len(compilers) > 1:
        raise CompilerDuplicateError(compiler_spec, arch_spec)
    return compilers[0]


@_auto_compiler_spec
def get_compiler_duplicates(compiler_spec, arch_spec):
    config_scopes = spack.config.config_scopes
    scope_to_compilers = dict()
    for scope in config_scopes:
        compilers = compilers_for_spec(compiler_spec, arch_spec=arch_spec,
                                       scope=scope, use_cache=False)
        if compilers:
            scope_to_compilers[scope] = compilers

    cfg_file_to_duplicates = dict()
    for scope, compilers in scope_to_compilers.iteritems():
        config_file = config_scopes[scope].get_section_filename('compilers')
        cfg_file_to_duplicates[config_file] = compilers

    return cfg_file_to_duplicates


def class_for_compiler_name(compiler_name):
    """Given a compiler module name, get the corresponding Compiler class."""
    assert(supported(compiler_name))

    file_path = join_path(spack.compilers_path, compiler_name + ".py")
    compiler_mod = imp.load_source(_imported_compilers_module, file_path)
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
            (x, len(y)) for x, y in config_file_to_duplicates.iteritems())
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
