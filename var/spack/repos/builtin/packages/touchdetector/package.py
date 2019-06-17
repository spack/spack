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
    version('5.0.1', tag='5.0.1', git=url, submodules=True)
    version('5.0.0', tag='5.0.0', git=url, submodules=True)
    version('4.4.2', tag='4.4.2', git=url, submodules=True)
    version('4.4.1', tag='4.4.1', git=url, submodules=True)
    version('4.3.3', tag='4.3.3', git=url, submodules=True)

    variant('openmp', default=False, description='Enables OpenMP support')

    depends_on('cmake', type='build')
    depends_on('boost@1.50:')
    depends_on('catch~single_header', when='@5.0.2:')
    depends_on('eigen', when='@4.5:')
    depends_on('fmt', when='@4.5:')
    depends_on('hdf5@1.8:')
    depends_on('morphio@2.0.8:', when='@4.5:')
    depends_on('mvdtool@1.5.1:', when='@4.5:')
    depends_on('mpi')
    depends_on('pugixml', when='@4.5:')
    depends_on('range-v3', when='@5.0.2:')

    # Old dependencies
    depends_on('hpctools~openmp', when='~openmp@:4.4')
    depends_on('hpctools+openmp', when='+openmp@:4.4')
    depends_on('libxml2', when='@:4.4')
    depends_on('zlib', when='@:4.4')

    def cmake_args(self):
        args = [
            '-DUSE_OPENMP:BOOL={}'.format('+openmp' in self.spec),
            '-DCMAKE_C_COMPILER={}'.format(self.spec['mpi'].mpicc),
            '-DCMAKE_CXX_COMPILER={}'.format(self.spec['mpi'].mpicxx)
        ]
        return args
