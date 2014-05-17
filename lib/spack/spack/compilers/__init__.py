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


@memoized
def supported_compilers():
    """Return a list of names of compilers supported by Spack.

       See available_compilers() to get a list of all the available
       versions of supported compilers.
    """
    return sorted(c for c in list_modules(spack.compilers_path))


def supported(compiler_spec):
    """Test if a particular compiler is supported."""
    if not isinstance(compiler_spec, spack.spec.CompilerSpec):
        compiler_spec = spack.spec.CompilerSpec(compiler_spec)
    return compiler_spec.name in supported_compilers()


def available_compilers():
    """Return a list of specs for all the compiler versions currently
       available to build with.  These are instances of
       CompilerSpec.
    """
    return [spack.spec.CompilerSpec(c)
            for c in list_modules(spack.compiler_version_path)]


def compiler_for_spec(compiler_spec):
    """This gets an instance of an actual spack.compiler.Compiler object
       from a compiler spec.  The spec needs to be concrete for this to
       work; it will raise an error if passed an abstract compiler.
    """
    matches = [c for c in available_compilers() if c.satisfies(compiler_spec)]

    # TODO: do something when there are zero matches.
    assert(len(matches) >= 1)

    compiler = matches[0]
    file_path = join_path(spack.compiler_version_path, "%s.py" % compiler)

    mod = imp.load_source(_imported_versions_module, file_path)
    compiler_class = class_for_compiler_name(compiler.name)

    return compiler_class(mod.cc, mod.cxx, mod.f77, mod.f90)


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
