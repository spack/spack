# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class Dpcpp(CMakePackage):
    """Data Parallel C++ compiler: Intel's implementation of SYCL programming model"""

    homepage = "https://intel.github.io/llvm-docs/"
    git = "https://github.com/intel/llvm.git"

    version("develop", branch="sycl")
    version("2023-03", sha256="ca85303d712c58316a91a7c97f7c78fa563a29f1669d8b2368d0c8bd92a63068", url="https://github.com/intel/llvm/tarball/cb91c232")
    version("2021.09", commit="bd68232bb96386bf7649345c0557ba520e73c02d")
    version("2021.12", commit="27f59d8906fcc8aece7ff6aa570ccdee52168c2d")

    maintainers("ravil-mobile")
    
    variant("cuda", default=False, description="switch from OpenCL to CUDA")
    variant("hip", default=False, description="switch from OpenCL to HIP")
    variant(
        "hip-platform",
        default="AMD",
        values=("AMD", "NVIDIA"),
        multi=False,
        description="choose HIP backend",
    )
    variant("esimd-emulator", default=False, description="build with ESIMD emulation support")
    variant("assertions", default=False, description="build with assertions")
    variant("docs", default=False, description="build Doxygen documentation")
    variant("werror", default=False, description="treat warnings as errors")
    variant("remangle_libclc", default=True, description="remangle libclc gen. variants")
    variant("shared-libs", default=False, description="build shared libraries")
    variant("lld", default=False, description="use LLD linker for build")
    variant("fusion", default=True, description="Enable the kernel fusion JIT compiler")

    depends_on("cmake@3.16.2:", type="build")
    depends_on("ninja@1.10.0:", type="build")

    depends_on("cuda@10.2.0:11.4.999", when="+cuda")

    # NOTE: AMD HIP needs to be tested; it will be done in the next update
    # depends_on('cuda@10.2.0:10.2.999', when='rocm-platform=NVIDIA', type='build')
    # depends_on('hip@4.0.0:', when='+rocm', type='build')

    root_cmakelists_dir = "llvm"

    def cmake_args(self):
        llvm_external_projects = "sycl;llvm-spirv;opencl;libdevice;xpti;xptifw"

        if "+fusion" in self.spec:
            llvm_external_projects += ";sycl-fusion"

        sycl_dir = os.path.join(self.stage.source_path, "sycl")
        spirv_dir = os.path.join(self.stage.source_path, "llvm-spirv")
        xpti_dir = os.path.join(self.stage.source_path, "xpti")
        xptifw_dir = os.path.join(self.stage.source_path, "xptifw")
        libdevice_dir = os.path.join(self.stage.source_path, "libdevice")
        fusion_dir = os.path.join(self.stage.source_path, "sycl-fusion")
        llvm_enable_projects = "clang;" + llvm_external_projects
        libclc_targets_to_build = ""
        sycl_build_pi_hip_platform = self.spec.variants["hip-platform"].value
        llvm_targets_to_build = get_llvm_targets_to_build(self.spec.target.family)
        sycl_enabled_plugins = "opencl"
        
        if self.spec.platform != "darwin":
            sycl_enabled_plugins += ";level_zero"

        is_cuda = "+cuda" in self.spec
        is_hip = "+hip" in self.spec

        if "+esimd-emulator" in self.spec:
            sycl_enabled_plugins += ";esimd_emulator"
        if is_cuda or is_hip:
            llvm_enable_projects += ";libclc"

        if is_cuda:
            llvm_targets_to_build += ";NVPTX"
            libclc_targets_to_build = "nvptx64--;nvptx64--nvidiacl"
            sycl_enabled_plugins += ";cuda"

        if is_hip:
            if sycl_build_pi_hip_platform == "AMD":
                llvm_targets_to_build += ";AMDGPU"
                libclc_targets_to_build += ";amdgcn--;amdgcn--amdhsa"
            elif sycl_build_pi_hip_platform and not is_cuda:
                llvm_targets_to_build += ";NVPTX"
                libclc_targets_to_build += ";nvptx64--;nvptx64--nvidiacl"
            sycl_enabled_plugins += ";hip"

        args = [
            self.define_from_variant("LLVM_ENABLE_ASSERTIONS", "assertions"),
            self.define("LLVM_TARGETS_TO_BUILD", llvm_targets_to_build),
            self.define("LLVM_EXTERNAL_PROJECTS", llvm_external_projects),
            self.define("LLVM_EXTERNAL_SYCL_SOURCE_DIR", sycl_dir),
            self.define("LLVM_EXTERNAL_LLVM_SPIRV_SOURCE_DIR", spirv_dir),
            self.define("LLVM_EXTERNAL_XPTI_SOURCE_DIR", xpti_dir),
            self.define("XPTI_SOURCE_DIR", xpti_dir),
            self.define("LLVM_EXTERNAL_XPTIFW_SOURCE_DIR", xptifw_dir),
            self.define("LLVM_EXTERNAL_LIBDEVICE_SOURCE_DIR", libdevice_dir),
            self.define("LLVM_EXTERNAL_SYCL_FUSION_SOURCE_DIR", fusion_dir),
            self.define("LLVM_ENABLE_PROJECTS", llvm_enable_projects),
            self.define("LIBCLC_TARGETS_TO_BUILD", libclc_targets_to_build),
            self.define("LLVM_BUILD_TOOLS", True),
            self.define_from_variant("SYCL_BUILD_PI_HIP_PLATFORM", "hip-platform"),
            self.define_from_variant("SYCL_ENABLE_WERROR", "werror"),
            self.define("SYCL_INCLUDE_TESTS", True),
            self.define_from_variant("LIBCLC_GENERATE_REMANGLED_VARIANTS", "remangle_libclc"),
            self.define_from_variant("LLVM_ENABLE_DOXYGEN", "docs"),
            self.define_from_variant("LLVM_ENABLE_SPHINX", "docs"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared-libs"),
            self.define("SYCL_ENABLE_XPTI_TRACING", "ON"),
            self.define_from_variant("LLVM_ENABLE_LLD", "lld"),
            self.define("SYCL_ENABLE_PLUGINS", sycl_enabled_plugins),
            self.define_from_variant("SYCL_ENABLE_KERNEL_FUSION", "fusion"),
        ]

        if is_cuda or (is_hip and sycl_build_pi_hip_platform == "NVIDIA"):
            args.append(self.define("CUDA_TOOLKIT_ROOT_DIR", self.spec["cuda"].prefix))

        if self.compiler.name == "gcc":
            gcc_prefix = ancestor(self.compiler.cc, 2)
            args.append(self.define("GCC_INSTALL_PREFIX", gcc_prefix))

        return args

    def setup_build_environment(self, env):
        if "+cuda" in self.spec:
            env.set("CUDA_LIB_PATH", "{0}/lib64/stubs".format(self.spec["cuda"].prefix))

    @run_after("install")
    def post_install(self):
        clang_cpp_path = os.path.join(self.spec.prefix.bin, "clang++")
        dpcpp_path = os.path.join(self.spec.prefix.bin, "dpcpp")

        real_clang_cpp_path = os.path.realpath(clang_cpp_path)
        os.symlink(real_clang_cpp_path, dpcpp_path)

    def setup_run_environment(self, env):
        bin_path = self.spec.prefix.bin
        for env_var_name, compiler in zip(["CC", "CXX"], ["clang", "clang++"]):
            env.set(env_var_name, os.path.join(bin_path, compiler))

        include_env_vars = ["C_INCLUDE_PATH", "CPLUS_INCLUDE_PATH", "INCLUDE"]
        for var in include_env_vars:
            env.prepend_path(var, self.prefix.include)
            env.prepend_path(var, self.prefix.include.sycl)

        sycl_build_pi_hip_platform = self.spec.variants["hip-platform"].value
        if "+cuda" in self.spec or sycl_build_pi_hip_platform == "NVIDIA":
            env.prepend_path("PATH", self.spec["cuda"].prefix.bin)
            env.set("CUDA_TOOLKIT_ROOT_DIR", self.spec["cuda"].prefix)

def get_llvm_targets_to_build(family):
    host_target = ""
    if family in ("x86", "x86_64"):
        host_target = "X86"
    elif family == "arm":
        host_target = "ARM"
    elif family == "aarch64":
        host_target = "AArch64"
    elif family in ("sparc", "sparc64"):
        host_target = "Sparc"
    elif family in ("ppc64", "ppc64le", "ppc", "ppcle"):
        host_target = "PowerPC"
    return host_target
