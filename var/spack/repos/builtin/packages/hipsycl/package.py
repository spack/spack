# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
from os import path

from llnl.util import filesystem

from spack.package import *


class Hipsycl(CMakePackage, CudaPackage, ROCmPackage):
    """hipSYCL is an implementation of the SYCL standard programming model
    over NVIDIA CUDA/AMD HIP"""

    homepage = "https://github.com/AdaptiveCpp/AdaptiveCpp"
    url = "https://github.com/AdaptiveCpp/AdaptiveCpp/archive/v23.10.0.tar.gz"
    git = "https://github.com/AdaptiveCpp/AdaptiveCpp.git"

    maintainers("nazavode")

    provides("sycl")

    license("BSD-2-Clause")

    version("stable", branch="stable", submodules=True)
    version("23.10.0", commit="3952b468c9da89edad9dff953cdcab0a3c3bf78c", submodules=True)
    version("0.9.4", commit="99d9e24d462b35e815e0e59c1b611936c70464ae", submodules=True)
    version("0.9.4", commit="99d9e24d462b35e815e0e59c1b611936c70464ae", submodules=True)
    version("0.9.3", commit="51507bad524c33afe8b124804091b10fa25618dc", submodules=True)
    version("0.9.2", commit="49fd02499841ae884c61c738610e58c27ab51fdb", submodules=True)
    version("0.9.1", commit="fe8465cd5399a932f7221343c07c9942b0fe644c", submodules=True)
    version("0.8.0", commit="2daf8407e49dd32ebd1c266e8e944e390d28b22a", submodules=True)
    version("develop", branch="develop", submodules=True)

    variant("opencl", default=False, description="Enable OpenCL backend for SYCL kernels")
    variant("sscp", default=False, description="Enable SSCP compiler")
    variant(
        "level_zero", default=False, description="Enable Intel Level Zero backend for SYCL kernels"
    )

    depends_on("cmake@3.5:", type="build")
    depends_on("boost +filesystem", when="@:0.8")
    depends_on("boost@1.67.0:1.69.0 +filesystem +fiber +context cxxstd=17", when="@0.9.1:")
    depends_on("python@3:")
    depends_on("llvm@8: +clang", when="~cuda")
    depends_on("llvm@9: +clang", when="+cuda")
    # hipSYCL 0.8.0 supported only LLVM 8-10:
    # (https://github.com/AdaptiveCpp/AdaptiveCpp/blob/v0.8.0/CMakeLists.txt#L29-L37)
    depends_on("llvm@8:10", when="@0.8.0")
    # https://github.com/OpenSYCL/OpenSYCL/pull/918 was introduced after 0.9.4
    conflicts("^llvm@16:", when="@:0.9.4")
    # LLVM PTX backend requires cuda7:10.1 (https://tinyurl.com/v82k5qq)
    depends_on("cuda@9:10.1", when="@0.8.1: +cuda ^llvm@9")
    depends_on("cuda@9:", when="@0.8.1: +cuda ^llvm@10:")
    # hipSYCL@:0.8.0 requires cuda@9:10.0 due to a known bug
    depends_on("cuda@9:10.0", when="@:0.8.0 +cuda")
    depends_on("llvm@9: +clang", when="+rocm")

    conflicts(
        "%gcc@:4",
        when="@:0.9.0",
        msg="hipSYCL needs proper C++14 support to be built, %gcc is too old",
    )
    conflicts(
        "%gcc@:8",
        when="@0.9.1:",
        msg="hipSYCL needs proper C++17 support to be built, %gcc is too old",
    )
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
            "-DWITH_ROCM_BACKEND:Bool={0}".format("TRUE" if "+rocm" in spec else "FALSE"),
            "-DWITH_CUDA_BACKEND:Bool={0}".format("TRUE" if "+cuda" in spec else "FALSE"),
            "-DWITH_LEVEL_ZERO_BACKEND:Bool={0}".format("TRUE" if "+intel" in spec else "FALSE"),
            "-DWITH_OPENCL_BACKEND:Bool={0}".format("TRUE" if "+opencl" in spec else "FALSE"),
            "-DWITH_SSCP_COMPILER:Bool={0}".format("TRUE" if "+sscp" in spec else "FALSE"),
            # prevent hipSYCL's cmake to look for other LLVM installations
            # if the specified one isn't compatible
            "-DDISABLE_LLVM_VERSION_CHECK:Bool=TRUE",
        ]
        if self.version >= Version("23.10.0"):
            args.append("-DACPP_VERSION_SUFFIX={0}".format(self.version))
        # LLVM directory containing all installed CMake files
        # (e.g.: configs consumed by client projects)
        llvm_cmake_dirs = filesystem.find(spec["llvm"].prefix.lib, "LLVMExports.cmake")
        if len(llvm_cmake_dirs) != 1:
            raise InstallError(
                "concretized llvm dependency must provide "
                "a unique directory containing CMake client "
                "files, found: {0}".format(llvm_cmake_dirs)
            )
        args.append("-DLLVM_DIR:String={0}".format(path.dirname(llvm_cmake_dirs[0])))

        # clang internal headers directory
        llvm_clang_include_dirs = filesystem.find(
            spec["llvm"].prefix.lib, "__clang_cuda_runtime_wrapper.h"
        )
        if len(llvm_clang_include_dirs) != 1:
            raise InstallError(
                "concretized llvm dependency must provide a "
                "unique directory containing clang internal "
                "headers, found: {0}".format(llvm_clang_include_dirs)
            )
        args.append(
            "-DCLANG_INCLUDE_PATH:String={0}".format(path.dirname(llvm_clang_include_dirs[0]))
        )
        # Find the right LLVM compiler
        llvm_clang_bin = path.join(spec["llvm"].prefix.bin, "clang")
        llvm_clang_bin_cpp = path.join(spec["llvm"].prefix.bin, "clang++")
        if not filesystem.is_exe(llvm_clang_bin):
            llvm_clang_bin = path.join(spec["llvm"].prefix.bin, "amdclang")
            llvm_clang_bin_cpp = path.join(spec["llvm"].prefix.bin, "amdclang++")
            if not filesystem.is_exe(llvm_clang_bin):
                raise InstallError(
                    "concretized LLVM dependency must provide a "
                    "valid clang/amdclang executable, found invalid: "
                    "{0}".format(llvm_clang_bin)
                )
        args.append("-DCLANG_EXECUTABLE_PATH:String={0}".format(llvm_clang_bin))
        args.append("-DCMAKE_C_COMPILER:String={0}".format(llvm_clang_bin))
        args.append("-DCMAKE_CXX_COMPILER:String={0}".format(llvm_clang_bin_cpp))

        # explicit CUDA toolkit
        if "+cuda" in spec:
            args.append("-DCUDA_TOOLKIT_ROOT_DIR:String={0}".format(spec["cuda"].prefix))
        if "+rocm" in spec:
            # FIXME: here spec["rocm"].prefix does not work
            # Instead (temporary solution: we use HIP prefix and
            # remove the "hip/" part of the path which is the ROCm path
            rocm_path = path.split(spec["hip"].prefix[:-1])[0]
            args.append("-DROCM_PATH:String={0}".format(rocm_path))

        return args

    @run_after("install")
    def filter_config_file(self):
        def edit_config(filename, editor):
            config_file_paths = filesystem.find(self.prefix, filename)
            if len(config_file_paths) != 1:
                raise InstallError(
                    "installed hipSYCL must provide a unique compiler driver"
                    "configuration file ({0}), found: {1}".format(filename, config_file_paths)
                )
            config_file_path = config_file_paths[0]
            with open(config_file_path) as f:
                config = json.load(f)

            config_modified = editor(config)

            with open(config_file_path, "w") as f:
                json.dump(config_modified, f, indent=2)

        if self.spec.satisfies("@:23.10.0"):
            configfiles = {"core": "syclcc.json", "cuda": "syclcc.json"}
        else:
            configfiles = {"core": "acpp-core.json", "cuda": "acpp-cuda.json"}

        def adjust_core_config(config):
            config["default-cpu-cxx"] = self.compiler.cxx
            return config

        edit_config(configfiles["core"], adjust_core_config)

        if self.spec.satisfies("+cuda"):
            # 1. Fix compiler: use the real one in place of the Spack wrapper

            # 2. Fix stdlib: we need to make sure cuda-enabled binaries find
            #    the libc++.so and libc++abi.so dyn linked to the sycl
            #    ptx backend
            rpaths = set()
            so_paths = filesystem.find_libraries(
                "libc++", self.spec["llvm"].prefix, shared=True, recursive=True
            )
            if len(so_paths) != 1:
                raise InstallError(
                    "concretized llvm dependency must provide a "
                    "unique directory containing libc++.so, "
                    "found: {0}".format(so_paths)
                )
            rpaths.add(path.dirname(so_paths[0]))
            so_paths = filesystem.find_libraries(
                "libc++abi", self.spec["llvm"].prefix, shared=True, recursive=True
            )
            if len(so_paths) != 1:
                raise InstallError(
                    "concretized llvm dependency must provide a "
                    "unique directory containing libc++abi, "
                    "found: {0}".format(so_paths)
                )
            rpaths.add(path.dirname(so_paths[0]))

            def adjust_cuda_config(config):
                config["default-cuda-link-line"] += " " + " ".join(
                    "-rpath {0}".format(p) for p in rpaths
                )
                return config

            edit_config(configfiles["cuda"], adjust_cuda_config)
