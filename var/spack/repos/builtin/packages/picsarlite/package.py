##############################################################################
# Copyright (c) 2018, Los Alamos National Security, LLC.
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


class Picsarlite(MakefilePackage):
    """PICSARlite is a self-contained proxy that adequately portrays the
       computational loads and dataflow of more complex PIC codes.
    """

    tags = ['proxy-app', 'ecp-proxy-app']

    homepage = "https://picsar.net"
    git      = "https://bitbucket.org/berkeleylab/picsar.git"

    version('develop', branch='PICSARlite')
    version('0.1', tag='PICSARlite-0.1')

    variant('prod', default=False, 
            description='Production mode (without FFTW)')
    variant('prod_spectral', default=False, 
            description='Production mode with spectral solver and FFTW')
    variant('debug', default=True, 
            description='Debug mode')
    variant('vtune', default=False, 
            description='Vtune profiling')
    variant('sde', default=False, 
            description='sde profiling')
    variant('map', default=False, 
            description='Allinea Map profiling')
    variant('library', default=False, 
            description='Create static and dynamic library')

    variant('cori2', default=False, 
            description='Build for cori2')
    variant('cori1', default=False, 
            description='Build for cori1')
    variant('edison', default=False, 
            description='Build for edison')
    variant('default', default=True, 
            description='Default build')

    variant('knl', default=False, 
            description='Build for knl architecture')
    variant('ivy', default=False, 
            description='Build for ivy bridge architecture')
    variant('hsw', default=False, 
            description='Build for haswell architecture')
    variant('host', default=True, 
            description='Build for the host architecture')

    depends_on('mpi')
    depends_on('fftw@3.0: +mpi', when='+prod_spectral')

    @property
    def build_targets(self):
        targets = []
        serial = '-j1'
        targets.append('FC={0}'.format(self.spec['mpi'].mpifc))
        targets.append('CC={0}'.format(self.spec['mpi'].mpicc))
        targets.append(format(serial))

        comp = 'user'
        vendors = {'%gcc': 'gnu', '%intel': 'intel'}
        for key, value in vendors.items():
            if self.spec.satisfies(key):
                comp = value
        targets.append('COMP={0}'.format(comp))

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

        if '+cori2' in self.spec:
            sys = 'cori2'
        elif '+cori1' in self.spec:
            sys = 'cori1'
        elif '+edison' in self.spec:
            sys = 'edison'
        elif '+default' in self.spec:
            sys = 'default'
        targets.append('SYS = {0}'.format(sys))

        if '+knl' in self.spec:
            arch = 'knl'
        elif '+ivy' in self.spec:
            arch = 'ivy'
        elif '+hsw' in self.spec:
            arch = 'hsw'
        elif '+host' in self .spec:
            arch = 'host'
        targets.append('ARCH = {0}'.format(arch))

        return targets

    def install(self, spec, prefix):
        install_tree('Acceptance_testing', prefix.Acceptance_testing)
        install_tree('performance_tests', prefix.performance_tests)
        install_tree('examples', prefix.examples)
        install_tree('python_module', prefix.python_module)
        install_tree('utils', prefix.utils)
        mkdirp(prefix.doc)
        install('README.md', prefix.doc)
        install('license.txt', prefix.doc)
