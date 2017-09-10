##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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

    # tr4-stable branch
    version('3.9.2b2',
            git='https://github.com/OpenMPToolsInterface/LLVM-openmp.git',
            commit='5cdca5dd3c0c336d42a335ca7cff622e270c9d47')
    # align-to-tr-rebased branch
    version('3.9.2b',
            git='https://github.com/OpenMPToolsInterface/LLVM-openmp.git',
            commit='982a08bcf3df9fb5afc04ac3bada47f19cc4e3d3')

    depends_on('cmake@2.8:', type='build')
    depends_on('llvm')
    depends_on('ninja@1.5:', type='build')

    generator = 'Ninja'

    def cmake_args(self):
        return [
            '-DCMAKE_C_COMPILER=clang',
            '-DCMAKE_CXX_COMPILER=clang++',
            '-DLIBOMP_OMPT_SUPPORT=on',
            '-DLIBOMP_OMPT_BLAME=on',
            '-DLIBOMP_OMPT_TRACE=on'
        ]
