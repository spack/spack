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


class Redset(CMakePackage):
    """Create MPI communicators for disparate redundancy sets"""

    homepage = "https://github.com/ECP-VeloC/redset"
    url      = "https://github.com/ECP-VeloC/redset/archive/v0.0.2.zip"
    git      = "https://github.com/ecp-veloc/redset.git"

    tags = ['ecp']

    version('master', branch='master')
    version('0.0.3', sha256='f110c9b42209d65f84a8478b919b27ebe2d566839cb0cd0c86ccbdb1f51598f4')

    depends_on('mpi')
    depends_on('rankstr')
    depends_on('kvtree+mpi')

    def cmake_args(self):
        args = []
        args.append("-DMPI_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        if self.spec.satisfies('platform=cray'):
            args.append("-DREDSET_LINK_STATIC=ON")
        args.append("-DWITH_KVTREE_PREFIX=%s" % self.spec['kvtree'].prefix)
        args.append("-DWITH_RANKSTR_PREFIX=%s" % self.spec['rankstr'].prefix)
        return args
