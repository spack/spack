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
from spack import *

class LlvmCompilerRt(Package):
    """Compiler-rt consists of several libraries to be used with LLVM:
          basics:
              A simple library that provides an implementation of the
              low-level target-specific hooks required by code
              generation and other runtime components.

          sanitizer runtimes:
              Runtime libraries that are required to run the code with
              sanitizer instrumentation.

          profiler:
              Library used to collect coverage information.

          BlocksRuntime:
              A target-independent implementation of Apple "Blocks"
              runtime interfaces.
    """
    homepage = "http://compiler-rt.llvm.org"
    url      = "http://llvm.org/releases/3.4/compiler-rt-3.4.src.tar.gz"

    depends_on("clang")
    depends_on("llvm")

    version('3.4', '7938353e3a3bda85733a165e7ac4bb84')

    def install(self, spec, prefix):
        cmake(".", *std_cmake_args)

        make()
        make("install")
