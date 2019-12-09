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

    version("master", branch="master", submodules=True)
    version("0.8.0", commit="2daf8407e49dd32ebd1c266e8e944e390d28b22a", submodules=True)

    variant("cuda", default=False, description="Enable CUDA backend for SYCL kernels")

    depends_on("cmake@3.5:", type="build")
    depends_on("boost +filesystem")
    depends_on("python@3:")
    depends_on("llvm@8: +clang", when="~cuda")
    depends_on("llvm@9: +clang", when="+cuda")
    # LLVM PTX backend requires cuda7:10.1.9999 (https://tinyurl.com/v82k5qq)
    depends_on("cuda@9:10.1.9999", when="@0.8.1: +cuda")
    # hipSYCL@:0.8.0 requires cuda@9:10.0.9999 due to a known bug
    depends_on("cuda@9:10.0.9999", when="@:0.8.0 +cuda")

    conflicts(
        "^llvm build_type=Debug",
        when="+cuda",
        msg="LLVM debug builds don't work with hipSYCL CUDA backend; for "
        "further info please refer to: "
        "https://github.com/illuhad/hipSYCL/blob/master/doc/install-cuda.md",
    )

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DWITH_CPU_BACKEND:Bool=TRUE",
            "-DWITH_ROCM_BACKEND:Bool=FALSE",
            "-DWITH_CUDA_BACKEND:Bool={0}".format(
                "TRUE" if "+cuda" in spec else "FALSE"
            ),
            "-DDISABLE_LLVM_VERSION_CHECK:Bool=TRUE",
            "-DLLVM_DIR:String={0}".format(
                path.dirname(filesystem.find(
                    spec["llvm"].prefix, "LLVMExports.cmake")[0]
                )
            ),
            "-DCLANG_EXECUTABLE_PATH:String={0}".format(
                path.join(spec["llvm"].prefix.bin, "clang")
            ),
            "-DCLANG_INCLUDE_PATH:String={0}".format(
                path.join(spec["llvm"].prefix.include, "clang")
            ),
        ]
        if "+cuda" in spec:
            args.append(
                "-DCUDA_TOOLKIT_ROOT_DIR:String={0}".format(
                    spec["cuda"].prefix)
            )
        return args
