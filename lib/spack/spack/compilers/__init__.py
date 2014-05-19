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
#
# This needs to be expanded for full compiler support.
#
import imp

from llnl.util.lang import memoized, list_modules
from llnl.util.filesystem import join_path

import spack
import spack.error
import spack.spec
from spack.compiler import Compiler
from spack.util.executable import which
from spack.util.naming import mod_to_class

_imported_compilers_module = 'spack.compiler.versions'
_imported_versions_module  = 'spack.compilers'


def _auto_compiler_spec(function):
    def converter(cspec_like):
        if not isinstance(cspec_like, spack.spec.CompilerSpec):
            cspec_like = spack.spec.CompilerSpec(cspec_like)
        return function(cspec_like)
    return converter


@memoized
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


@memoized
def all_compilers():
    """Return a set of specs for all the compiler versions currently
       available to build with.  These are instances of CompilerSpec.
    """
    return set(spack.spec.CompilerSpec(c)
               for c in list_modules(spack.compiler_version_path))


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
    matches = find(compiler_spec)

    compilers = []
    for cspec in matches:
        path = join_path(spack.compiler_version_path, "%s.py" % cspec)
        mod  = imp.load_source(_imported_versions_module, path)
        cls  = class_for_compiler_name(cspec.name)
        compilers.append(cls(mod.cc, mod.cxx, mod.f77, mod.fc))

    return compilers


@_auto_compiler_spec
def compiler_for_spec(compiler_spec):
    assert(compiler_spec.concrete)
    compilers = compilers_for_spec(compiler_spec)
    assert(len(compilers) == 1)
    return compilers[0]


def class_for_compiler_name(compiler_name):
    assert(supported(compiler_name))

    file_path = join_path(spack.compilers_path, compiler_name + ".py")
    compiler_mod = imp.load_source(_imported_compilers_module, file_path)
    return getattr(compiler_mod, mod_to_class(compiler_name))


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
