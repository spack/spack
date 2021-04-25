# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rmgdft(CMakePackage, CudaPackage, ROCmPackage):
    """RMGDFT is a high performance real-space density functional code
       designed for large scale electronic structure calculations."""

    homepage = "http://www.rmgdft.org/"
    git      = "https://github.com/RMGDFT/rmgdft.git"
    maintainers = ['elbriggs']
    tags = ['ecp', 'ecp-apps']
    version('master')

    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo'))
    variant('cuda', default=False,
            description='Build with cuda support.')
    variant('hip', default=False,
            description='Build with hip/rocm support.')
    variant('qmcpack', default=True,
            description='Build with qmcpack interface.')

    # RMGDFT 4.0.0 or later requires support for C++14
    compiler_warning = 'RMGDFT 4.0.0 or later requires a ' \
                       'compiler with support for C++14'
    conflicts('%gcc@:4', when='@3.6.0:', msg=compiler_warning)
    conflicts('%intel@:17', when='@3.6.0:', msg=compiler_warning)
    conflicts('%pgi@:17', when='@3.6.0:', msg=compiler_warning)
    conflicts('%llvm@:3.4', when='@3.6.0:', msg=compiler_warning)

    conflicts(
        '+hip',
        when='+cuda',
        msg='RMGDFT cannot be built with cuda and hip at the same time.')

    depends_on('cmake@3.18.1', type='build')
    depends_on('boost@1.74.0:')
    depends_on('fftw-api@3')
    depends_on('openblas threads=none')
    depends_on('mpi')
    depends_on('hdf5')

    @property
    def build_targets(self):
        spec = self.spec
        if '+hip' in spec:
            targets = ['rmg-gpu']
        elif '+cuda' in spec:
            targets = ['rmg-gpu']
        else:
            targets = ['rmg-cpu']
        return targets

    def cmake_args(self):
        spec = self.spec
        args = []
        if '+hip' in spec:
            args.append('-DRMG_HIP_ENABLED=1')
        if '+cuda' in spec:
            args.append('-DRMG_CUDA_ENABLED=1')
            cuda_arch_list = spec.variants['cuda_arch'].value
            cuda_arch = cuda_arch_list[0]
            if len(cuda_arch_list) > 1:
                raise InstallError(
                    'RMGDFT only supports compilation for a single '
                    'GPU architecture at a time'
                )
            if cuda_arch != 'none':
                args.append('-DCUDA_ARCH=sm_{0}'.format(cuda_arch))
            else:
                args.append('-DCUDA_ARCH=sm_60')

        else:
            args.append('-DRMG_CUDA_ENABLED=0')

        return args

    def install(self, spec, prefix):

        env['CC'] = spec['mpi'].mpicc
        env['CXX'] = spec['mpi'].mpicxx
        env['F77'] = spec['mpi'].mpif77
        env['FC'] = spec['mpi'].mpifc

        # create top-level directories
        mkdirp(prefix.bin)
        mkdirp(prefix.share.tests.RMG)

        # install binary
        if '+cuda' in spec:
            with working_dir(self.build_directory):
                install('rmg-gpu', prefix.bin)
        elif '+hip' in spec:
            with working_dir(self.build_directory):
                install('rmg-gpu', prefix.bin)
        else:
            with working_dir(self.build_directory):
                install('rmg-cpu', prefix.bin)

        # install tests
        with working_dir(self.build_directory):
            install_tree('tests/RMG', prefix.share.tests.RMG)
