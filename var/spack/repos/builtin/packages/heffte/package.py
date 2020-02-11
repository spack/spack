# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Heffte(CMakePackage):
    """Highly Efficient FFT for Exascale"""

    homepage = "https://bitbucket.org/icl/heffte"
    url      = "https://bitbucket.org/icl/heffte/get/v0.1.tar.gz"
    git      = "https://bitbucket.org/icl/heffte.git"

    version('master', branch='master')
    version('0.2', sha256='4e76ae60982b316c2e873b2e5735669b22620fefa1fc82f325cdb6989bec78d1')
    version('0.1', sha256='d279a03298d2dc76574b1ae1031acb4ea964348cf359273d1afa4668b5bfe748')

    variant('cuda', default=False, description='Builds with support for GPUs via CUDA')

    depends_on('fftw')
    depends_on('mpi')
    depends_on('cuda', when="+cuda")

    def cmake_args(self):
        args = ['-DBUILD_SHARED=ON']
        if '+cuda' in self.spec:
            args.append('-DBUILD_GPU=ON')
        else:
            args.append('-DBUILD_GPU=OFF')
        return args
