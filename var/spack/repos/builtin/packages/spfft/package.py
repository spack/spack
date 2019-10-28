# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Spfft(CMakePackage):
    """Sparse 3D FFT library with MPI, OpenMP, CUDA and ROCm support."""

    homepage = "https://github.com/eth-cscs/SpFFT"
    url      = "https://github.com/eth-cscs/SpFFT/archive/v0.9.8.zip"

    version('0.9.8', sha256='f49fa51316bbfa68309e951d2375e1f6904120c93868cbe13bc2974c0b801a3f')

    variant('openmp', default=True, description="Build with OpenMP support")
    variant('mpi', default=True, description="enable MPI")
    variant('single_precision', default=False, description="Sinlge precision")
    variant('gpu_direct', default=False, description="GPU aware MPI")
    variant('static', default=False, description="build static library")
    variant('cuda', default=False, description="CUDA")
    variant('build_type', default='Release', description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo'))
    depends_on('fftw')
    depends_on('mpi', when='+mpi')
    depends_on('cuda', when='+cuda')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('+openmp'):
            args += ["-DSPFFT_OMP=On"]
        if self.spec.satisfies('+mpi'):
            args += ["-DSPFFT_MPI=On"]
        if self.spec.satisfies('+single_precision'):
            args += ["-DSPFFT_SINGLE_PRECISION=On"]
        if self.spec.satisfies('+gpu_direct'):
            args += ["-DSPFFT_GPU_DIRECT=On"]
        if self.spec.satisfies('+cuda'):
            args += ["-DSPFFT_BACKEND=CUDA"]
        if self.spec.satisfies('+cuda'):
            args += ["-DSPFFT_BACKEND=CUDA"]
        return args
