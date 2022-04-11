# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Arrayfire(CMakePackage, CudaPackage):
    """ArrayFire is a high performance software library for parallel computing
    with an easy-to-use API. Its array based function set makes parallel
    programming more accessible."""

    homepage = "https://arrayfire.org/docs/index.htm"
    git      = "https://github.com/arrayfire/arrayfire.git"
    maintainers = ['umar456']

    version('master')
    version('3.8.1', tag='v3.8.1')
    version('3.7.3', submodules=True, tag='v3.7.3')
    version('3.7.2', submodules=True, tag='v3.7.2')
    version('3.7.0', submodules=True, tag='v3.7.0')

    variant('cuda',   default=False, description='Enable CUDA backend')
    variant('forge',  default=False, description='Enable graphics library')
    variant('opencl', default=False, description='Enable OpenCL backend')

    depends_on('boost@1.70:')
    depends_on('fftw-api@3:')
    depends_on('blas')
    depends_on('cuda@7.5:', when='+cuda')
    depends_on('cudnn', when='+cuda')
    depends_on('opencl +icd', when='+opencl')
    # TODO add more opencl backends:
    # currently only Cuda backend is enabled
    # https://github.com/arrayfire/arrayfire/wiki/Build-Instructions-for-Linux#opencl-backend-dependencies

    depends_on('fontconfig', when='+forge')
    depends_on('glfw@3.1.4:', when='+forge')

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters

        libraries = []
        if 'cpu' in query_parameters:
            libraries.append('libafcpu')
        if 'cuda' in query_parameters and '+cuda' in self.spec:
            libraries.append('libafcuda')
        if 'opencl' in query_parameters and '+opencl' in self.spec:
            libraries.append('libafopencl')
        if not query_parameters or 'unified' in query_parameters:
            libraries.append('libaf')

        return find_libraries(libraries, root=self.prefix, recursive=True)

    def cmake_args(self):
        args = []
        args.extend([
            self.define_from_variant('AF_BUILD_CUDA', 'cuda'),
            self.define_from_variant('AF_BUILD_FORGE', 'forge'),
            self.define_from_variant('AF_BUILD_OPENCL', 'opencl'),
            self.define('BUILD_TESTING', self.run_tests),
        ])

        if '+cuda' in self.spec:
            cuda_arch_list = self.spec.variants['cuda_arch'].value
            cuda_arch = cuda_arch_list[0]
            if cuda_arch != 'none':
                arch_list_string = ['{}.{}'.format(arch[:-1], arch[-1])
                                    for arch in cuda_arch_list]
                args.append(self.define('CUDA_architecture_build_targets',
                                        arch_list_string))

        if '^mkl' in self.spec:
            if self.version >= Version('3.8.0'):
                args.append(self.define('AF_COMPUTE_LIBRARY', 'Intel-MKL'))
            else:
                args.append(self.define('USE_CPU_MKL', True))
                args.append(self.define('USE_OPENCL_MKL', True))
            if '%intel' not in self.spec:
                args.append(self.define('MKL_THREAD_LAYER', 'GNU OpenMP'))
        else:
            if self.version >= Version('3.8.0'):
                args.append(self.define('AF_COMPUTE_LIBRARY', 'FFTW/LAPACK/BLAS'))
            else:
                args.append(self.define('USE_CPU_MKL', False))
                args.append(self.define('USE_OPENCL_MKL', False))

        return args
