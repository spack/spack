# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Mercury(CMakePackage):
    """Mercury is a C library for implementing RPC, optimized for HPC"""

    homepage = 'https://mercury-hpc.github.io/'
    url = 'https://github.com/mercury-hpc/mercury/archive/0.9.0.tar.gz'
    git = 'https://github.com/mercury-hpc/mercury.git'

    version('develop', branch='master', submodules=True)
    version('1.0.1', tag='v1.0.1', submodules=True)
    version('1.0.0', tag='v1.0.0', submodules=True)
    version('0.9.0', tag='v0.9.0', submodules=True)

    variant('bmi', default=False, description='Use BMI for network transport')
    variant('cci', default=False, description='Use CCI for network transport')
    variant('mpi', default=False, description='Use MPI for network transport')
    variant('ofi', default=True,  description='Use libfabric plugin')
    variant('sm',  default=False, description='Use shared-memory plugin')
    variant('opa', default=False, description='Use OpenPA for atomics')
    variant('boost', default=True, description='Use BOOST preprocessor macros')
    variant('selfforward', default=True,
            description='Mercury will short-circuit operations' +
                        ' by forwarding to itself when possible')
    # NOTE: the 'udreg' variant requires that the MPICH_GNI_NDREG_ENTRIES=1024
    #   environment variable be set at run time to avoid conflicts with
    #   Cray-MPICH if libfabric and MPI are used at the same time
    variant('udreg', default=False,
            description='Enable udreg on supported Cray platforms')

    depends_on('cmake@2.8.12.2:', type='build')
    # depends_on('bmi', when='+bmi')  # TODO: add BMI package
    # depends_on('cci', when='+cci')  # TODO: add CCI package
    depends_on('mpi', when='+mpi')
    depends_on('libfabric@1.5:', when='+ofi')
    depends_on('openpa@1.0.3:', when='+opa')
    depends_on('boost@1.48:', when='+boost')

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DBUILD_SHARED_LIBS=ON',
            '-DMERCURY_USE_CHECKSUMS=ON',
            '-DMERCURY_USE_EAGER_BULK=ON',
            '-DMERCURY_USE_SYSTEM_MCHECKSUM=OFF',
            '-DMERCURY_USE_XDR=OFF'
        ]

        if '+boost' in spec:
            args.append('-DMERCURY_USE_BOOST_PP=ON')
        else:
            args.append('-DMERCURY_USE_BOOST_PP=OFF')

        if '+bmi' in spec:
            args.append('-DNA_USE_BMI=ON')
        else:
            args.append('-DNA_USE_BMI=OFF')

        if '+cci' in spec:
            args.append('-DNA_USE_CCI=ON')
        else:
            args.append('-DNA_USE_CCI=OFF')

        if '+mpi' in spec:
            args.append('-DNA_USE_MPI=ON')
        else:
            args.append('-DNA_USE_MPI=OFF')

        if '+ofi' in spec:
            args.append('-DNA_USE_OFI=ON')
            if self.run_tests:
                args.append('-DNA_OFI_TESTING_PROTOCOL={0}'.format(';'.join(
                    spec['libfabric'].variants['fabrics'].value)))
        else:
            args.append('-DNA_USE_OFI=OFF')

        if '+sm' in spec:
            args.append('-DNA_USE_SM=ON')
        else:
            args.append('-DNA_USE_SM=OFF')

        if '+opa' in spec:
            args.append('-DMERCURY_USE_OPA=ON')
        else:
            args.append('-DMERCURY_USE_OPA=OFF')

        if '+selfforward' in spec:
            args.append('-DMERCURY_USE_SELF_FORWARD=ON')
        else:
            args.append('-DMERCURY_USE_SELF_FORWARD=OFF')

        if '+udreg' in spec:
            args.append('-DNA_OFI_GNI_USE_UDREG=ON')
        else:
            args.append('-DNA_OFI_GNI_USE_UDREG=OFF')

        if self.run_tests:
            args.append('-DBUILD_TESTING=ON')
        else:
            args.append('-DBUILD_TESTING=OFF')

        if '+mpi' in spec and self.run_tests:
            args.append('-DMERCURY_ENABLE_PARALLEL_TESTING=ON')
        else:
            args.append('-DMERCURY_ENABLE_PARALLEL_TESTING=OFF')

        return args

    def check(self):
        """Unit tests fail when run in parallel."""

        with working_dir(self.build_directory):
            make('test', parallel=False)
