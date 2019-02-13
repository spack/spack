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


class Touchdetector(CMakePackage):
    """Detects autaptic touches between branches
    """
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/building/TouchDetector"
    url      = "ssh://bbpcode.epfl.ch/building/TouchDetector"

    version('develop', git=url, submodules=True)
    version('4.4.0', tag='4.4.0', git=url, submodules=True, preferred=True)
    version('4.3.3', tag='4.3.3', git=url, submodules=True)

    variant('openmp', default=False, description='Enables OpenMP support')

    depends_on('boost@1.50:')
    depends_on('cmake', type='build')
    depends_on('hpctools~openmp', when='~openmp')
    depends_on('hpctools+openmp', when='+openmp')
    depends_on('hdf5@1.8:')
    depends_on('libxml2')
    depends_on('mpi')
    depends_on('zlib')

    def cmake_args(self):
        args = [
            '-DUSE_OPENMP:BOOL={}'.format('+openmp' in self.spec),
            '-DCMAKE_C_COMPILER={}'.format(self.spec['mpi'].mpicc),
            '-DCMAKE_CXX_COMPILER={}'.format(self.spec['mpi'].mpicxx)
        ]
        return args
