##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class LlvmOpenmpOmpt(CMakePackage):
    """The OpenMP subproject provides an OpenMP runtime for use with the
       OpenMP implementation in Clang. This branch includes experimental
       changes for OMPT, the OpenMP Tools interface"""

    homepage = "https://github.com/OpenMPToolsInterface/LLVM-openmp"

    # towards_tr4 branch
    version('towards_tr4', branch='towards_tr4',
            git='https://github.com/OpenMPToolsInterface/LLVM-openmp.git')

    version('3.9.2b2',
            git='https://github.com/OpenMPToolsInterface/LLVM-openmp.git',
            commit='5cdca5dd3c0c336d42a335ca7cff622e270c9d47')

    # align-to-tr-rebased branch
    version('3.9.2b',
            git='https://github.com/OpenMPToolsInterface/LLVM-openmp.git',
            commit='982a08bcf3df9fb5afc04ac3bada47f19cc4e3d3')

    # variant for building llvm-openmp-ompt as a stand alone library
    variant('standalone', default=False,
            description="Build llvm openmpi ompt library as a \
                         stand alone entity.")

    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    depends_on('cmake@2.8:', type='build')
    depends_on('llvm', when='~standalone')
    depends_on('ninja@1.5:', type='build')

    generator = 'Ninja'

    def cmake_args(self):
        cmake_args = [
            '-DLIBOMP_OMPT_SUPPORT=on',
            '-DLIBOMP_OMPT_BLAME=on',
            '-DLIBOMP_OMPT_TRACE=on',
            '-DCMAKE_C_COMPILER=%s' % spack_cc,
            '-DCMAKE_CXX_COMPILER=%s' % spack_cxx
        ]

        # Build llvm-openmp-ompt as a stand alone library
        # CMAKE rpath variable prevents standalone error
        # where this package wants the llvm tools path
        if '+standalone' in self.spec:
                cmake_args.extend(
                    ['-DLIBOMP_STANDALONE_BUILD=true',
                     '-DCMAKE_BUILD_WITH_INSTALL_RPATH=true',
                     '-DLIBOMP_USE_DEBUGGER=false'])

        # Build llvm-openmp-ompt using the toward_tr4 branch
        # This requires the version to be 5.0 (50)
        if '@towards_tr4' in self.spec:
                cmake_args.extend(
                    ['-DLIBOMP_OMP_VERSION=50'])

        return cmake_args
