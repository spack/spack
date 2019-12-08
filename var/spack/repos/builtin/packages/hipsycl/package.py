# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from os import path
from llnl.util import filesystem


class Hipsycl(CMakePackage):
    """hipSYCL is an implementation of the SYCL standard programming model
    over NVIDIA CUDA/AMD HIP"""

    homepage = "https://github.com/illuhad/hipSYCL"
    url = "https://github.com/illuhad/hipSYCL/archive/v0.8.0.tar.gz"
    git = "https://github.com/illuhad/hipSYCL.git"

    maintainers = ["nazavode"]

    provides("sycl")

    version("master", branch="master")
    version(
        "0.8.0",
        sha256="4ec5218103d1b38efae9a51ca752b9b44bbd02dada78c05e20e00c9c25e9ea19",
    )

    variant("cuda", default=False, description="Enable CUDA backend for SYCL kernels")

    depends_on("boost +filesystem")
    depends_on("python@3:")
    depends_on("llvm@8:", when="~cuda")
    # LLVM debug builds don't work with hipSYCL CUDA backend:
    # https://github.com/illuhad/hipSYCL/blob/master/doc/install-cuda.md
    depends_on("llvm@9: build_type=Release", when="+cuda")
    # hipSYCL requires cuda@9:
    # LLVM PTX backend requires cuda7:10.1.9999 (https://tinyurl.com/v82k5qq)
    depends_on("cuda@9:10.1.9999", when="+cuda")

    depends_on("cmake@3.5:", type="build")

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DLLVM_DIR:String={0}".format(
                path.dirname(
                    filesystem.find(spec["llvm"].prefix, "LLVMExports.cmake"))
            ),
            "-DCLANG_EXECUTABLE_PATH:String={0}".format(
                path.join(spec["llvm"].bin, "clang")
            ),
            "-DCLANG_INCLUDE_PATH:String={0}".format(
                path.join(spec["llvm"].include, "clang")
            ),
        ]
        if "+cuda" in spec:
            args.append(
                "-DCUDA_TOOLKIT_ROOT_DIR:String={0}".format(
                    spec["cuda"].prefix)
            )
        return args
