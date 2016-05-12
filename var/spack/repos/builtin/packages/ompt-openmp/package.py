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
from spack import *

class OmptOpenmp(Package):
    """LLVM/Clang OpenMP runtime with OMPT support. This is a fork of the OpenMPToolsInterface/LLVM-openmp fork of the official LLVM OpenMP mirror.  This library provides a drop-in replacement of the OpenMP runtimes for GCC, Intel and LLVM/Clang."""
    homepage = "https://github.com/OpenMPToolsInterface/LLVM-openmp"
    url      = "http://github.com/khuck/LLVM-openmp/archive/v0.1.tar.gz"

    version('0.1', '2334e6a84b52da41b27afd9831ed5370')

    # depends_on("foo")

    def install(self, spec, prefix):
        with working_dir("runtime/build", create=True):

            # FIXME: Modify the configure line to suit your build system here.
            cmake('-DCMAKE_C_COMPILER=%s' % self.compiler.cc, 
                  '-DCMAKE_CXX_COMPILER=%s' % self.compiler.cxx,
                  '-DCMAKE_INSTALL_PREFIX=%s' % prefix,
                  '..', *std_cmake_args)

            # FIXME: Add logic to build and install here
            make()
            make("install")
