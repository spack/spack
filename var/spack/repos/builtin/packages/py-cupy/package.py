# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCupy(PythonPackage, CudaPackage):
    """CuPy is an open-source array library accelerated with
    NVIDIA CUDA. CuPy provides GPU accelerated computing with
    Python. CuPy uses CUDA-related libraries including cuBLAS,
    cuDNN, cuRand, cuSolver, cuSPARSE, cuFFT and NCCL to make
    full use of the GPU architecture."""

    homepage = "https://cupy.dev/"
    pypi = "cupy/cupy-8.0.0.tar.gz"

    version("11.2.0", sha256="c33361f117a347a63f6996ea97446d17f1c038f1a1f533e502464235076923e2")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.29.22:2", type="build")
    depends_on("py-fastrlock@0.5:", type=("build", "run"))
    depends_on("py-numpy@1.20:1.25", type=("build", "run"))
    depends_on("cuda")
    depends_on("nccl")
    depends_on("cudnn")
    depends_on("cutensor")

    conflicts("~cuda")

    def setup_build_environment(self, env):
        env.set("CUPY_NUM_BUILD_JOBS", make_jobs)
        if not self.spec.satisfies("cuda_arch=none"):
            cuda_arch = self.spec.variants["cuda_arch"].value
            arch_str = ";".join("arch=compute_{0},code=sm_{0}".format(i) for i in cuda_arch)
            env.set("CUPY_NVCC_GENERATE_CODE", arch_str)
