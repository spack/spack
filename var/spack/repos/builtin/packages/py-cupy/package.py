# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCupy(PythonPackage):
    """CuPy is an open-source array library accelerated with
    NVIDIA CUDA. CuPy provides GPU accelerated computing with
    Python. CuPy uses CUDA-related libraries including cuBLAS,
    cuDNN, cuRand, cuSolver, cuSPARSE, cuFFT and NCCL to make
    full use of the GPU architecture."""

    homepage = "https://cupy.dev/"
    pypi = "cupy/cupy-8.0.0.tar.gz"

    version("11.2.0", sha256="c33361f117a347a63f6996ea97446d17f1c038f1a1f533e502464235076923e2")
    version(
        "8.0.0",
        sha256="d1dcba5070dfa754445d010cdc952ff6b646d5f9bdcd7a63e8246e2472c3ddb8",
        deprecated=True,
    )

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.29.22:2", type="build")
    depends_on("py-fastrlock@0.5:", type=("build", "run"))
    depends_on("py-numpy@1.20:1.25", type=("build", "run"))
    depends_on("cuda")
    depends_on("nccl")
    depends_on("cudnn")
    depends_on("cutensor")
