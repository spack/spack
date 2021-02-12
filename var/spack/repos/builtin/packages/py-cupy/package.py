# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCupy(PythonPackage):
    """CuPy is an open-source array library accelerated with
    NVIDIA CUDA. CuPy provides GPU accelerated computing with
    Python. CuPy uses CUDA-related libraries including cuBLAS,
    cuDNN, cuRand, cuSolver, cuSPARSE, cuFFT and NCCL to make
    full use of the GPU architecture."""

    homepage = "https://cupy.dev/"
    pypi = "cupy/cupy-8.0.0.tar.gz"

    version('8.4.0', sha256='58d19af6b2e83388d4f0f6ca4226bae4b947920d2ca4951c2eddc8bc78abf66b')
    version('8.3.0', sha256='db699fddfde7806445908cf6454c6f4985e7a9563b40405ddf97845d808c5f12')
    version('8.2.0', sha256='8e4bc8428fb14309d73194e19bc4b47e1d6a330678a200e36d9d4b932f1be2e8')
    version('8.1.0', sha256='4dfa4a0cd0a752d980347c816cab2169f0938c1d37275311810396dcf3c27912')
    version('8.0.0', sha256='d1dcba5070dfa754445d010cdc952ff6b646d5f9bdcd7a63e8246e2472c3ddb8')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-fastrlock@0.3:', type=('build', 'run'))
    depends_on('py-numpy@1.15:', type=('build', 'run'))
    depends_on('cuda')
    depends_on('nccl')
    depends_on('cudnn')
