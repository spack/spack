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
from llnl.util.lang import memoized, list_modules

import spack
import spack.spec
from spack.util.executable import which

@memoized
def supported_compilers():
    """Return a list of names of compilers supported by Spack.

       See available_compilers() to get a list of all the available
       versions of supported compilers.
    """
    return sorted(c for c in list_modules(spack.compilers_path))


def available_compilers():
    """Return a list of specs for all the compiler versions currently
       available to build with.  These are instances of
       spack.spec.Compiler.
    """
    return [spack.spec.Compiler(c)
            for c in list_modules(spack.compiler_version_path)]


def supported(compiler_spec):
    """Test if a particular compiler is supported."""
    if not isinstance(compiler_spec, spack.spec.Compiler):
        compiler_spec = spack.spec.Compiler(compiler_spec)
    return compiler_spec.name in supported_compilers()


@memoized
def default_compiler():
    """Get the spec for the default compiler supported by Spack.
       Currently just returns the system's default gcc.

       TODO: provide a better way to specify/find this on startup.
    """
    gcc = which('gcc', required=True)
    version = gcc('-dumpversion', return_output=True)
    return spack.spec.Compiler('gcc', version)
