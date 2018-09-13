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
import llnl.util.tty as tty


class Swiftsim(AutotoolsPackage):
    """SPH With Inter-dependent Fine-grained Tasking (SWIFT) provides
    astrophysicists with a state of the art framework to perform
    particle based simulations.
    """

    homepage = 'http://icc.dur.ac.uk/swift/'
    url = 'https://gitlab.cosma.dur.ac.uk/api/v4/projects/swift%2Fswiftsim/repository/archive.tar.gz?sha=v0.3.0'

    version('0.7.0', '1c703d7e20a31a3896e1c291bddd71ab')
    version('0.3.0', '162ec2bdfdf44a31a08b3fcee23a886a')

    variant('mpi', default=True,
            description='Enable distributed memory parallelism')

    # Build dependencies
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    # link-time / run-time dependencies
    depends_on('mpi', when='+mpi')
    depends_on('metis')
    depends_on('hdf5~mpi', when='~mpi')
    depends_on('hdf5+mpi', when='+mpi')

    def setup_environment(self, spack_env, run_env):
        # Needed to be able to download from the Durham gitlab repository
        tty.warn('Setting "GIT_SSL_NO_VERIFY=1"')
        tty.warn('This is needed to clone SWIFT repository')
        spack_env.set('GIT_SSL_NO_VERIFY', 1)

    def configure_args(self):
        return ['--prefix=%s' % self.prefix,
                '--enable-mpi' if '+mpi' in self.spec else '--disable-mpi',
                '--with-metis={0}'.format(self.spec['metis'].prefix),
                '--enable-optimization']
