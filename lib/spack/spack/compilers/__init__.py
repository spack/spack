##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""This module contains functions related to finding compilers on the
system and configuring Spack to use multiple compilers.
"""
import imp
import os

from llnl.util.lang import memoized, list_modules
from llnl.util.filesystem import join_path

import spack
import spack.error
import spack.spec
import spack.config

from spack.util.multiproc import parmap
from spack.compiler import Compiler
from spack.util.executable import which
from spack.util.naming import mod_to_class
from spack.util.environment import get_path

_imported_compilers_module = 'spack.compilers'
_required_instance_vars = ['cc', 'cxx', 'f77', 'fc']

_default_order = ['gcc', 'intel', 'pgi', 'clang', 'xlc']

def _auto_compiler_spec(function):
    def converter(cspec_like):
        if not isinstance(cspec_like, spack.spec.CompilerSpec):
            cspec_like = spack.spec.CompilerSpec(cspec_like)
        return function(cspec_like)
    return converter


def _get_config():
    """Get a Spack config, but make sure it has compiler configuration
       first."""
    # If any configuration file has compilers, just stick with the
    # ones already configured.
    config = spack.config.get_compilers_config()
    existing = [spack.spec.CompilerSpec(s)
                for s in config]
    if existing:
        return config

    compilers = find_compilers(*get_path('PATH'))
    add_compilers_to_config('user', *compilers)

    # After writing compilers to the user config, return a full config
    # from all files.
    return spack.config.get_compilers_config()


_cached_default_compiler = None
def default_compiler():
    global _cached_default_compiler
    if _cached_default_compiler:
        return _cached_default_compiler
    versions = []
    for name in _default_order:  # TODO: customize order.
        versions = find(name)
        if versions: break

    if not versions:
        raise NoCompilersError()

    _cached_default_compiler = sorted(versions)[-1]
    return _cached_default_compiler


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


def add_compilers_to_config(scope, *compilers):
    compiler_config_tree = {}
    for compiler in compilers:
        compiler_entry = {}
        for c in _required_instance_vars:
            val = getattr(compiler, c)
            if not val:
                val = "None"
            compiler_entry[c] = val
        compiler_config_tree[str(compiler.spec)] = compiler_entry
    spack.config.add_to_compiler_config(compiler_config_tree, scope)



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


def all_compilers():
    """Return a set of specs for all the compiler versions currently
       available to build with.  These are instances of CompilerSpec.
    """
    configuration = _get_config()
    return [spack.spec.CompilerSpec(s) for s in configuration]


@_auto_compiler_spec
def find(compiler_spec):
    """Return specs of available compilers that match the supplied
       compiler spec.  Return an list if nothing found."""
    return [c for c in all_compilers() if c.satisfies(compiler_spec)]


@_auto_compiler_spec
def compilers_for_spec(compiler_spec):
    """This gets all compilers that satisfy the supplied CompilerSpec.
       Returns an empty list if none are found.
    """
    config = _get_config()

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

        return cls(cspec, *compiler_paths)

    matches = find(compiler_spec)
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
