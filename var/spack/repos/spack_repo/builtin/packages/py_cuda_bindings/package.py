# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyCudaBindings(PythonPackage):
    """NVIDIA’s CUDA Python provides Cython bindings and Python wrappers for the
    driver and runtime API for existing toolkits and libraries to simplify
    GPU-based accelerated processing."""

    homepage = "https://github.com/NVIDIA/cuda-python"
    git = "https://github.com/NVIDIA/cuda-python"
    url = "https://github.com/NVIDIA/cuda-python/releases/download/v12.9.0/cuda-python-v12.9.0.tar.gz"

    version("12.9.0", sha256="1fa57a9fad278256cbb3b6cf347d2b258a7f83bba2759257e54c9fabd0b07ce1")
    version("12.8.0", sha256="6cc8db1e65a1f995e289b64f9b9bff4362321d36ecf9b54eb192d0781475fbca")
    version("11.8.7", sha256="613ec6d0cde3db4d48074010ed6015ff60462f14c5fa7d8fe82fe7a7ecd5d1ac")

    depends_on("cuda@12.9", when="@12.9.0")
    depends_on("cuda@12.8", when="@12.8.0")
    depends_on("cuda@11.8", when="@11.8.7")
    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-cython", type="build")
    depends_on("py-pyclibrary", type=("build", "run"))
    depends_on("py-pywin32", when="platform=windows", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@77.0.0:", when="@12.9.0", type="build")

    build_directory = "cuda_bindings"

    def setup_build_environment(self, env):
        cuda_version = self.spec["cuda"].version
        if cuda_version >= Version("12.9"):
            env.append_path("LIBRARY_PATH", self.spec["cuda"].prefix.lib64)
