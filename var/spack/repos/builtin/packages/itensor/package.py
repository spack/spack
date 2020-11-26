# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Itensor(MakefilePackage):
    """ITensor -Intelligent Tensor- is a library for
    implementing tensor network calculations."""

    homepage = "https://itensor.org/index.html"
    url      = "https://github.com/ITensor/ITensor/archive/v3.1.6.tar.gz"

    version('3.1.6', sha256='1c42cd39c45124063d9812b851b4d99735caff7ac2da971b4287c2018d4cf32a')
    version('3.1.5', sha256='a0661efdda3bfc4fab1796243d4b438b0f17adce08b6bb21a2aaae9766b6a1ec')
    version('3.1.4', sha256='bdcfa786f5165b6f5d1a40a80e7ecca2e59e2ee7050fd60f42ef4a4a55a793c5')
    version('3.1.3', sha256='ff6b04f9c642c6795acd3485f44619282a2dde7a49a4e0dee89b47b69dc3853e')
    version('3.1.2', sha256='3e0f032c211e11be1b5a4adf4a581698a949d03b35c0e9b2e3d9f4bab6dd7967')
    version('3.1.1', sha256='3c12d288e50522b5bd152f956a48ec187486cfeb4ccb1ea9a05d3f0bf3bf8059')
    version('3.1.0', sha256='b887cb9c7fc06f60d9d6834380b643adea8d165d574ab1859883f399725b9db9')
    version('3.0.1', sha256='5e2ac3a5b62fb3e34f1e520e6da911b56659507fb4143118d4a602a5866bc912')
    version('3.0.0', sha256='1d249a3a6442188a9f7829b32238c1025457c2930566d134a785994b1f7c54a9')
    version('2.1.1', sha256='b91a67af66ed0fa7678494f3895b5d5ae7f1dc1026540689f9625f515cb7791c')

    variant('blaslapack', default='openblas', values=('openblas',
            'mkl', 'lapack', 'macos', 'fjssl2'),
            description='Enable the use of OpenBlas/MKL/Lapack or MacOS.')
    variant('openmp', default=False, description='Enable OpenMP support.')
    variant('hdf5', default=False, description='Build rockstar with HDF5 support.')

    depends_on('openblas', when='blaslapack=openblas')
    depends_on('intel-mkl', when='blaslapack=mkl')
    depends_on('netlib-lapack', when='blaslapack=lapack')

    depends_on('hdf5+hl', when='+hdf5')

    def edit(self, spec, prefix):
        # 0.copy config.mk
        mf = 'options.mk'
        copy('options.mk.sample', mf)

        # 1.CCCOM
        ccopts = 'CCCOM={0}'.format(spack_cxx)
        if spec.satisfies('%gcc'):
            if not spec.satisfies('arch=aarch64:'):
                ccopts += ' -m64'
            ccopts += ' -std=c++17 -fconcepts -fPIC'
        if spec.satisfies('%clang') or spec.satisfies('%fj'):
            ccopts += ' -std=c++17 -fPIC -Wno-gcc-compat'
        filter_file(r'^CCCOM.+', ccopts, mf)

        # 2.BLAS/LAPACK
        btype = self.spec.variants['blaslapack'].value
        if btype == 'openblas':
            vpla = 'PLATFORM=openblas'
            vlib = 'BLAS_LAPACK_LIBFLAGS=-lpthread -lopenblas'
            vinc = 'BLAS_LAPACK_INCLUDEFLAGS=-fpermissive '
            vinc += '-DHAVE_LAPACK_CONFIG_H -DLAPACK_COMPLEX_STRUCTURE'
            filter_file(r'^PLATFORM.+', vpla, mf)
            filter_file(r'^BLAS_LAPACK_LIB.+', vlib, mf)
            filter_file('#PLATFORM=lapack', vinc, mf, String=True)

        # 3.HDF5
        if '+hdf5' in spec:
            hdf5p = 'HDF5_PREFIX={0}'.format(spec["hdf5"].prefix.lib)
            filter_file('^#HDF5.+', hdf5p, mf)

        # 4.openmp
        if '+openmp' in spec:
            filter_file('#ITENSOR_USE_OMP', 'ITENSOR_USE_OMP', mf)

        # prefix
        filter_file(
            r'^PREFIX.+',
            'PREFIX={0}'.format(os.getcwd()),
            mf
        )
