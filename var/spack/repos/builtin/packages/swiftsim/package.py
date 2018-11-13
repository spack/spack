# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
