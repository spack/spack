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


class Aluminum(CMakePackage):
    """Aluminum provides a generic interface to high-performance
    communication libraries, with a focus on allreduce
    algorithms. Blocking and non-blocking algorithms and GPU-aware
    algorithms are supported. Aluminum also contains custom
    implementations of select algorithms to optimize for certain
    situations."""

    homepage = "https://github.com/LLNL/Aluminum"
    url      = "https://github.com/LLNL/Aluminum/archive/v0.1.tar.gz"
    git      = "https://github.com/LLNL/Aluminum.git"

    version('master', branch='master')
    version('0.1', sha256='3880b736866e439dd94e6a61eeeb5bb2abccebbac82b82d52033bc6c94950bdb')

    variant('gpu', default=False, description='Builds with support for GPUs via CUDA and cuDNN')
    variant('nccl', default=False, description='Builds with support for NCCL communication lib')
    variant('mpi_cuda', default=False, description='Builds with support for MPI-CUDA enabled library')

    depends_on('cuda', when='+gpu')
    depends_on('cudnn', when='+gpu')
    depends_on('cub', when='+gpu')
    depends_on('mpi', when='~mpi_cuda')
    depends_on('mpi +cuda', when='+mpi_cuda')
    depends_on('nccl', when='+nccl')

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DALUMINUM_ENABLE_CUDA:BOOL=%s' % ('+gpu' in spec),
            '-DALUMINUM_ENABLE_MPI_CUDA:BOOL=%s' % ('+mpi_cuda' in spec),
            '-DALUMINUM_ENABLE_NCCL:BOOL=%s' % ('+nccl' in spec)]
        return args
