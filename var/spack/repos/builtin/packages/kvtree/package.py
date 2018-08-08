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


class Kvtree(CMakePackage):
    """KVTree provides a fully extensible C datastructure modeled after perl
    hashes."""

    homepage = "https://github.com/ECP-VeloC/KVTree"
    url      = "https://github.com/ECP-VeloC/KVTree/archive/v1.0.1.zip"
    git      = "https://github.com/ecp-veloc/kvtree.git"

    tags = ['ecp']

    version('master', branch='master')
    version('1.0.2', sha256='6b54f4658e5ebab747c0c2472b1505ac1905eefc8a0b2a97d8776f800ee737a3')

    variant('mpi', default=True, description="Build with MPI message packing")
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('+mpi'):
            args.append("-DMPI=ON")
            args.append("-DMPI_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        else:
            args.append("-DMPI=OFF")
        if self.spec.satisfies('platform=cray'):
            args.append("-DKVTREE_LINK_STATIC=ON")
        return args
