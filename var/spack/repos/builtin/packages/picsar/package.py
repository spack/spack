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


class Picsar(MakefilePackage):
    """PICSAR is a high performance library of optimized versions of the key
       functionalities of the PIC loop.
    """

    homepage = "https://picsar.net"
    git      = "https://bitbucket.org/berkeleylab/picsar.git"

    version('develop', branch='master')

    variant('prod', default=True, description='Production mode (without FFTW)')
    variant('prod_spectral', default=False,
            description='Production mode with spectral solver and FFTW')
    variant('debug', default=False, description='Debug mode')
    variant('vtune', default=False, description='Vtune profiling')
    variant('sde', default=False, description='sde profiling')
    variant('map', default=False, description='Allinea Map profiling')
    variant('library', default=False, 
            description='Create static and dynamic library')

    depends_on('mpi')
    depends_on('fftw@3.0: +mpi', when='+prod_spectral')

    parallel = False

    @property
    def build_targets(self):
        targets = []
        targets.append('FC={0}'.format(self.spec['mpi'].mpifc))
        targets.append('CC={0}'.format(self.spec['mpi'].mpicc))

        comp = 'user'
        vendors = {'%gcc': 'gnu', '%intel': 'intel'}
        for key, value in vendors.items():
            if self.spec.satisfies(key):
                comp = value
        targets.append('COMP={0}'.format(comp))
        if comp is 'user':
            targets.append('FARGS={0}{1}'.format('-g -O3 ',
                           self.compiler.openmp_flag))

        if '+prod' in self.spec:
            mode = 'prod'
        elif '+prod_spectral' in self.spec:
            mode = 'prod_spectral'
        elif '+debug' in self.spec:
            mode = 'debug'
        elif '+vtune' in self.spec:
            mode = 'vtune'
        elif '+sde' in self.spec:
            mode = 'sde'
        elif '+map' in self.spec:
            mode = 'map'
        elif '+library' in self.spec:
            mode = 'library'
        targets.append('MODE = {0}'.format(mode))

        targets.append('SYS = default')

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.docs)
        install('README.md', prefix.docs)

        mkdirp(prefix.bin)
        install('fortran_bin/picsar', prefix.bin)
