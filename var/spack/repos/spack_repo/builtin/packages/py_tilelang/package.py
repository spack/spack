# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.python import PythonPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *


class PyTilelang(PythonPackage, CudaPackage, ROCmPackage):
    """Domain-specific language designed to streamline
    the development of high-performance GPU/CPU/Accelerators kernels"""

    license("MIT")
    homepage = "https://tilelang.com/"
    git = "https://github.com/tile-ai/tilelang.git"
    submodules = True

    # Exact set of modules is version- and variant-specific, just attempt to import the
    # core libraries to ensure that the package was successfully installed.
    import_modules = ["tilelang", "tilelang.language", "tilelang.intrinsics"]

    version("main", branch="main")
    version("0.1.5", tag="v0.1.5")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("patchelf", type="build")
    depends_on("cmake@3.26:", type="build")
    depends_on("py-packaging", type="build")
    depends_on("py-setuptools@61:", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-cython", type=["build", "run"])
    depends_on("py-decorator", type=["build", "run"])
    depends_on("py-numpy@1.23.5:", type=["build", "run"])
    depends_on("py-tqdm@4.62.3:", type=["build", "run"])
    depends_on("py-typing-extensions@4.10.0:", type=["build", "run"])
    depends_on("py-attrs", type=["build", "run"])
    depends_on("py-cloudpickle", type=["build", "run"])
    depends_on("py-ml-dtypes", type=["build", "run"])
    depends_on("py-psutil", type=["build", "run"])
    depends_on("py-torch@2.2.0:", type=["build", "run"])

    def cmake_args(self):
        return [
            self.define_from_variant("USE_CUDA", "cuda"),
            self.define_from_variant("USE_ROCM", "rocm"),
        ]

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        if self.spec.satisfies("+cuda"):
            env.prepend_path("LD_LIBRARY_PATH", self.spec["cuda"].prefix.lib64)
