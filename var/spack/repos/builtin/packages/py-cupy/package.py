# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    git      = "https://github.com/cupy/cupy"

    version('8.0.0', tag='v8.0.0', submodules=True)

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-fastrlock@0.3:', type=('build', 'run'))
    depends_on('py-numpy@1.15:', type=('build', 'run'))
    depends_on('cuda')
    depends_on('nccl')
    depends_on('cudnn')
