##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
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
import imp

from llnl.util.lang import memoized, list_modules
from llnl.util.filesystem import join_path

import spack
import spack.error
import spack.spec
import spack.config

from spack.compiler import Compiler
from spack.util.executable import which
from spack.util.naming import mod_to_class

_imported_compilers_module = 'spack.compilers'
_required_instance_vars = ['cc', 'cxx', 'f77', 'fc']


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
    config = spack.config.get_config()
    existing = [spack.spec.CompilerSpec(s)
                for s in config.get_section_names('compiler')]
    if existing:
        return config

    user_config = spack.config.get_config('user')

    compilers = find_default_compilers()
    for name, clist in compilers.items():
        for compiler in clist:
            if compiler.spec not in existing:
                add_compiler(user_config, compiler)
    user_config.write()

    # After writing compilers to the user config, return a full config
    # from all files.
    return spack.config.get_config()


def add_compiler(config, compiler):
    def setup_field(cspec, name, exe):
        path = ' '.join(exe.exe) if exe else "None"
        config.set_value('compiler', cspec, name, path)

    for c in _required_instance_vars:
        setup_field(compiler.spec, c, getattr(compiler, c))


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
    return [spack.spec.CompilerSpec(s)
            for s in configuration.get_section_names('compiler')]


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
        items = { k:v for k,v in config.items('compiler "%s"' % cspec) }

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
        return cls(*compiler_paths)

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


def find_default_compilers():
    """Search the user's environment to get default compilers.  Each
       compiler class can have its own find() class method that can be
       customized to locate that type of compiler.
    """
    # Compiler name is inserted on load by class_for_compiler_name
    return {
        Compiler.name : [Compiler(*c) for c in Compiler.find()]
        for Compiler in all_compiler_types() }


@memoized
def default_compiler():
    """Get the spec for the default compiler on the system.
       Currently just returns the system's default gcc.

       TODO: provide a more sensible default.  e.g. on Intel systems
             we probably want icc.  On Mac OS, clang.  Probably need
             to inspect the system and figure this out.
    """
    gcc = which('gcc', required=True)
    version = gcc('-dumpversion', return_output=True)
    return spack.spec.CompilerSpec('gcc', version)


class InvalidCompilerConfigurationError(spack.error.SpackError):
    def __init__(self, compiler_spec):
        super(InvalidCompilerConfigurationError, self).__init__(
            "Invalid configuration for [compiler \"%s\"]: " % compiler_spec,
            "Compiler configuration must contain entries for all compilers: %s"
            % _required_instance_vars)
