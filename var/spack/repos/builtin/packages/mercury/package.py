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
    version('1.0.0', tag='v1.0.0', submodules=True)
    version('0.9.0', tag='v0.9.0', submodules=True)

    variant('cci', default=False, description='Use CCI for network transport')
    variant('bmi', default=False, description='Use BMI for network transport')
    variant('fabric', default=True, description='Use libfabric for network transport')
    variant('selfforward', default=True,
            description='Mercury will short-circuit operations' +
                        ' by forwarding to itself when possible')
# NOTE: the 'udreg' variant requires that the MPICH_GNI_NDREG_ENTRIES=1024
#   environment variable be set at run time to avoid conflicts with
#   Cray-MPICH if libfabric and MPI are used at the same time
    variant('udreg', default=False,
            description='Enable udreg on supported Cray platforms')

    depends_on('cci@master', when='+cci', type=('build', 'link', 'run'))
    depends_on('libfabric', when='+fabric', type=('build', 'link', 'run'))
    depends_on('bmi', when='+bmi', type=('build', 'link', 'run'))
    depends_on('openpa', type=('build', 'link', 'run'))

    def cmake_args(self):
        args = ['-DMERCURY_USE_BOOST_PP:BOOL=ON',
                '-DBUILD_SHARED_LIBS=ON']

        if (self.spec.variants['cci'].value):
            args.extend(['-DNA_USE_CCI:BOOL=ON'])
        else:
            args.extend(['-DNA_USE_CCI:BOOL=OFF'])

        if (self.spec.variants['bmi'].value):
            args.extend(['-DNA_USE_BMI:BOOL=ON'])
        else:
            args.extend(['-DNA_USE_BMI:BOOL=OFF'])

        if (self.spec.variants['fabric'].value):
            args.extend(['-DNA_USE_OFI:BOOL=ON'])
        else:
            args.extend(['-DNA_USE_OFI:BOOL=OFF'])

        if (self.spec.variants['selfforward'].value):
            args.extend(['-DMERCURY_USE_SELF_FORWARD=ON'])
        else:
            args.extend(['-DMERCURY_USE_SELF_FORWARD=OFF'])

        if (self.spec.variants['udreg'].value):
            args.extend(['-DNA_OFI_GNI_USE_UDREG=ON'])
        else:
            args.extend(['-DNA_OFI_GNI_USE_UDREG=OFF'])

        return args
