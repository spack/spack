# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class XsdkExamples(CMakePackage, CudaPackage):
    """xSDK Examples show usage of libraries in the xSDK package."""

    homepage = 'http://xsdk.info'
    url      = 'https://github.com/xsdk-project/xsdk-examples/archive/v0.1.0.tar.gz'
    git      = "https://github.com/xsdk-project/xsdk-examples"

    maintainers = ['acfisher', 'balay', 'balos1', 'luszczek']

    version('develop', branch='master')
    version('0.3.0', branch='balos1/updates')
    version('0.2.0', sha256='cf26e3a16a83eba6fb297fb106b0934046f17cf978f96243b44d9d17ad186db6')
    version('0.1.0', sha256='d24cab1db7c0872b6474d69e598df9c8e25d254d09c425fb0a6a8d6469b8018f')

    depends_on('xsdk+cuda', when='+cuda')
    for sm_ in CudaPackage.cuda_arch_values:
        depends_on('xsdk+cuda cuda_arch={0}'.format(sm_),
                   when='+cuda cuda_arch={0}'.format(sm_))

    depends_on('xsdk@develop', when='@develop')
    depends_on('xsdk@0.7.0', when='@0.3.0')
    depends_on('xsdk@0.7.0 ^mfem+strumpack', when='@0.3.0 ^xsdk+strumpack')
    depends_on('xsdk@0.7.0 ^sundials+magma', when='@0.3.0 +cuda')
    depends_on('xsdk@0.6.0', when='@0.2.0')
    depends_on('xsdk@0.5.0', when='@0.1.0')
    depends_on('mpi')
    depends_on('cmake@3.21:', type='build', when='@0.3.0:')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DENABLE_HYPRE=ON',
            '-DHYPRE_DIR=%s' % spec['hypre'].prefix,
            '-DENABLE_MFEM=ON',
            '-DMETIS_DIR=%s' % spec['metis'].prefix,
            '-DMFEM_DIR=%s' % spec['mfem'].prefix,
            '-DENABLE_PETSC=ON',
            '-DPETSc_DIR=%s' % spec['petsc'].prefix,
            '-DENABLE_PLASMA=ON',
            '-DPLASMA_DIR=%s' % spec['plasma'].prefix,
            '-DENABLE_SUNDIALS=ON',
            '-DSUNDIALS_DIR=%s' % spec['sundials'].prefix,
            '-DENABLE_SUPERLU=ON',
            '-DSUPERLUDIST_DIR=%s' % spec['superlu-dist'].prefix
        ]

        if '+cuda' in spec:  # if cuda variant was activated for xsdk
            args.extend([
                '-DENABLE_CUDA=ON',
                '-DCMAKE_CUDA_ARCHITECTURES=%s' % spec.variants['cuda_arch'].value
            ])
        if '+ginkgo' in spec:  # if ginkgo variant was activated for xsdk
            args.extend([
                '-DENABLE_GINKGO=ON',
                '-DGinkgo_DIR=%s' % spec['ginkgo'].prefix
            ])
        if '+magma' in spec:  # if magma variant was activated for xsdk
            args.extend([
                '-DENABLE_MAGMA=ON',
                '-DMAGMA_DIR=%s' % spec['magma'].prefix
            ])
        if '+strumpack' in spec:  # if magma variant was activated for xsdk
            args.extend([
                '-DENABLE_STRUMPACK=ON',
                '-DSTRUMPACK_DIR=%s' % spec['strumpack'].prefix
            ])
        if '+slate' in spec:  # if slate variant was activated for xsdk
            args.extend([
                '-DENABLE_SLATE=ON',
                '-DSLATE_DIR=%s' % spec['slate'].prefix,
                '-DBLASPP_DIR=%s' % spec['blaspp'].prefix,
                '-DLAPACKPP_DIR=%s' % spec['lapackpp'].prefix
            ])
        if 'trilinos' in spec:  # if trilinos variant was activated for xsdk
            args.extend([
                'ENABLE_TRILINOS=ON',
                '-DTRILINOS_DIR_PATH=%s' % spec['trilinos'].prefix
            ])
        if 'zlib' in spec:  # if zlib variant was activated for MFEM
            args.append('-DZLIB_LIBRARY_DIR=%s' % spec['zlib'].prefix.lib)

        return args
