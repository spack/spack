##############################################################################
# Copyright (c) 2018, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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


class Miniqmc(CMakePackage):
    """a simplified real space QMC code for algorithm development,
       performance portability testing, and computer science experiments
    """

    homepage = "https://github.com/QMCPACK/miniqmc"
    url      = "https://github.com/QMCPACK/miniqmc/archive/0.2.0.tar.gz"

    version('0.2.0', 'b96bacaf48b8e9c0de05d04a95066bc1')

    tags = ['proxy-app']

    depends_on('mpi')
    depends_on('lapack')

    def cmake_args(self):
        args = [
            '-DCMAKE_CXX_COMPILER=%s' % self.spec['mpi'].mpicxx,
            '-DCMAKE_C_COMPILER=%s' % self.spec['mpi'].mpicc
        ]
        return args

    def install(self, spec, prefix):
        install_tree(join_path('spack-build', 'bin'), prefix.bin)
        install_tree(join_path('spack-build', 'lib'), prefix.lib)
