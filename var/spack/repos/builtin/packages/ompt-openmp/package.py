##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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


class OmptOpenmp(CMakePackage):
    """LLVM/Clang OpenMP runtime with OMPT support. This is a fork of the
       OpenMPToolsInterface/LLVM-openmp fork of the official LLVM OpenMP
       mirror.  This library provides a drop-in replacement of the OpenMP
       runtimes for GCC, Intel and LLVM/Clang.

    """
    homepage = "https://github.com/OpenMPToolsInterface/LLVM-openmp"
    url      = "http://github.com/khuck/LLVM-openmp/archive/v0.1.tar.gz"

    version('0.1', '59d6933a2e9b7d1423fb9c7c77d5663f')

    depends_on('cmake@2.8:', type='build')

    conflicts('%gcc@:4.7')

    root_cmakelists_dir = 'runtime'
