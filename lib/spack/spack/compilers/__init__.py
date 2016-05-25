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
import os
import platform

from llnl.util.lang import memoized, list_modules
from llnl.util.filesystem import join_path

import spack
import spack.error
import spack.spec
import spack.config
import spack.architecture

from spack.util.multiproc import parmap
from spack.compiler import Compiler
from spack.util.executable import which
from spack.util.naming import mod_to_class
from spack.util.environment import get_path

_imported_compilers_module = 'spack.compilers'
_required_instance_vars = ['cc', 'cxx', 'f77', 'fc']

# TODO: customize order in config file
if platform.system() == 'Darwin':
    _default_order = ['clang', 'gcc', 'intel']
else:
    _default_order = ['gcc', 'intel', 'pgi', 'clang', 'xlc', 'nag']


def _auto_compiler_spec(function):
    def converter(cspec_like, *args, **kwargs):
        if not isinstance(cspec_like, spack.spec.CompilerSpec):
            cspec_like = spack.spec.CompilerSpec(cspec_like)
        return function(cspec_like, *args, **kwargs)
    return converter


def _to_dict(compiler):
    """Return a dict version of compiler suitable to insert in YAML."""
    return {
        str(compiler.spec) : dict(
            (attr, getattr(compiler, attr, None))
            for attr in _required_instance_vars)
    }


def get_compiler_config(arch=None, scope=None):
    """Return the compiler configuration for the specified architecture.
    """
    # Check whether we're on a front-end (native) architecture.
    my_arch = spack.architecture.sys_type()
    if arch is None:
        arch = my_arch

    def init_compiler_config():
        """Compiler search used when Spack has no compilers."""
        config[arch] = {}
        compilers = find_compilers(*get_path('PATH'))
        for compiler in compilers:
            config[arch].update(_to_dict(compiler))
        spack.config.update_config('compilers', config, scope=scope)

    config = spack.config.get_config('compilers', scope=scope)

    # Update the configuration if there are currently no compilers
    # configured.  Avoid updating automatically if there ARE site
    # compilers configured but no user ones.
    if arch == my_arch and arch not in config:
        if scope is None:
            # We know no compilers were configured in any scope.
            init_compiler_config()
        elif scope == 'user':
            # Check the site config and update the user config if
            # nothing is configured at the site level.
            site_config = spack.config.get_config('compilers', scope='site')
            if not site_config:
                init_compiler_config()

    return config[arch] if arch in config else {}


def add_compilers_to_config(compilers, arch=None, scope=None):
    """Add compilers to the config for the specified architecture.

    Arguments:
      - compilers: a list of Compiler objects.
      - arch:      arch to add compilers for.
      - scope:     configuration scope to modify.
    """
    if arch is None:
        arch = spack.architecture.sys_type()

    compiler_config = get_compiler_config(arch, scope)
    for compiler in compilers:
        compiler_config[str(compiler.spec)] = dict(
            (c, getattr(compiler, c, "None"))
            for c in _required_instance_vars)

    update = { arch : compiler_config }
    spack.config.update_config('compilers', update, scope)


@_auto_compiler_spec
def remove_compiler_from_config(compiler_spec, arch=None, scope=None):
    """Remove compilers from the config, by spec.

    Arguments:
      - compiler_specs: a list of CompilerSpec objects.
      - arch:           arch to add compilers for.
      - scope:          configuration scope to modify.
    """
    if arch is None:
        arch = spack.architecture.sys_type()

    compiler_config = get_compiler_config(arch, scope)
    del compiler_config[str(compiler_spec)]
    update = { arch : compiler_config }

    spack.config.update_config('compilers', update, scope)


def all_compilers_config(arch=None, scope=None):
    """Return a set of specs for all the compiler versions currently
       available to build with.  These are instances of CompilerSpec.
    """
    # Get compilers for this architecture.
    arch_config = get_compiler_config(arch, scope)

    # Merge 'all' compilers with arch-specific ones.
    # Arch-specific compilers have higher precedence.
    merged_config = get_compiler_config('all', scope=scope)
    merged_config = spack.config._merge_yaml(merged_config, arch_config)

    return merged_config


def all_compilers(arch=None, scope=None):
    # Return compiler specs from the merged config.
    return [spack.spec.CompilerSpec(s)
            for s in all_compilers_config(arch, scope)]


def default_compiler():
    versions = []
    for name in _default_order:
        versions = find(name)
        if versions:
            break
    else:
        raise NoCompilersError()

    return sorted(versions)[-1]


def find_compilers(*path):
    """Return a list of compilers found in the suppied paths.
       This invokes the find() method for each Compiler class,
       and appends the compilers detected to a list.
    """
    # Make sure path elements exist, and include /bin directories
    # under prefixes.
    filtered_path = []
    for p in path:
        # Eliminate symlinks and just take the real directories.
        p = os.path.realpath(p)
        if not os.path.isdir(p):
            continue
        filtered_path.append(p)

        # Check for a bin directory, add it if it exists
        bin = join_path(p, 'bin')
        if os.path.isdir(bin):
            filtered_path.append(os.path.realpath(bin))

    # Once the paths are cleaned up, do a search for each type of
    # compiler.  We can spawn a bunch of parallel searches to reduce
    # the overhead of spelunking all these directories.
    types = all_compiler_types()
    compiler_lists = parmap(lambda cls: cls.find(*filtered_path), types)

    # ensure all the version calls we made are cached in the parent
    # process, as well.  This speeds up Spack a lot.
    clist = reduce(lambda x,y: x+y, compiler_lists)
    return clist


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
def find(compiler_spec, arch=None, scope=None):
    """Return specs of available compilers that match the supplied
       compiler spec.  Return an list if nothing found."""
    return [c for c in all_compilers(arch, scope) if c.satisfies(compiler_spec)]


@_auto_compiler_spec
def compilers_for_spec(compiler_spec, arch=None, scope=None):
    """This gets all compilers that satisfy the supplied CompilerSpec.
       Returns an empty list if none are found.
    """
    config = all_compilers_config(arch, scope)

    def get_compiler(cspec):
        items = config[str(cspec)]

        if not all(n in items for n in _required_instance_vars):
            raise InvalidCompilerConfigurationError(cspec)

        cls  = class_for_compiler_name(cspec.name)
        compiler_paths = []
        for c in _required_instance_vars:
            compiler_path = items[c]
            if compiler_path != "None":
                compiler_paths.append(compiler_path)
            else:
                compiler_paths.append(None)

        flags = {}
        for f in spack.spec.FlagMap.valid_compiler_flags():
            if f in items:
                flags[f] = items[f]
        return cls(cspec, *compiler_paths, **flags)

    matches = find(compiler_spec, arch, scope)
    return [get_compiler(cspec) for cspec in matches]


@_auto_compiler_spec
def compiler_for_spec(compiler_spec):
    """Get the compiler that satisfies compiler_spec.  compiler_spec must
       be concrete."""
    assert(compiler_spec.concrete)
    compilers = compilers_for_spec(compiler_spec)
    assert(len(compilers) == 1)
    return compilers[0]


def class_for_compiler_name(compiler_name):
    """Given a compiler module name, get the corresponding Compiler class."""
    assert(supported(compiler_name))

    file_path = join_path(spack.compilers_path, compiler_name + ".py")
    compiler_mod = imp.load_source(_imported_compilers_module, file_path)
    cls = getattr(compiler_mod, mod_to_class(compiler_name))

    # make a note of the name in the module so we can get to it easily.
    cls.name = compiler_name

    return cls


def all_compiler_types():
    return [class_for_compiler_name(c) for c in supported_compilers()]


class InvalidCompilerConfigurationError(spack.error.SpackError):
    def __init__(self, compiler_spec):
        super(InvalidCompilerConfigurationError, self).__init__(
            "Invalid configuration for [compiler \"%s\"]: " % compiler_spec,
            "Compiler configuration must contain entries for all compilers: %s"
            % _required_instance_vars)


class NoCompilersError(spack.error.SpackError):
    def __init__(self):
        super(NoCompilersError, self).__init__("Spack could not find any compilers!")
