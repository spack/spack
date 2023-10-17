# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys

from spack.package import *


class Dpcpp(CMakePackage):
    """Data Parallel C++ compiler: Intel's implementation of SYCL programming model"""

    homepage = "https://intel.github.io/llvm-docs/"
    git = "https://github.com/intel/llvm.git"

    version("develop", branch="sycl")
    version(
        "2023-03",
        sha256="ca85303d712c58316a91a7c97f7c78fa563a29f1669d8b2368d0c8bd92a63068",
        url="https://github.com/intel/llvm/tarball/cb91c232",
    )

    version("2021.09", commit="bd68232bb96386bf7649345c0557ba520e73c02d", deprecated=True)
    version("2021.12", commit="27f59d8906fcc8aece7ff6aa570ccdee52168c2d", deprecated=True)

    maintainers("ravil-mobile")

    variant("cuda", default=False, description="switch from OpenCL to CUDA")
    variant("rocm", default=False, description="switch from OpenCL to HIP")
    variant("esimd-emulator", default=False, description="build with ESIMD emulation support")
    variant("assertions", default=False, description="build with assertions")
    variant("docs", default=False, description="build Doxygen documentation")
    variant("werror", default=False, description="treat warnings as errors")
    variant("shared-libs", default=False, description="build shared libraries")
    variant("lld", default=False, description="use LLD linker for build")
    variant("fusion", default=True, description="Enable the kernel fusion JIT compiler")
    variant(
        "security_flags",
        default="none",
        values=("none", "default", "sanitize"),
        multi=False,
        description="Enables security flags for compile & link",
    )
    variant(
        "llvm-external-projects",
        values=str,
        default="none",
        description="Add external projects to build. Add as a comma seperated list.",
    )

    depends_on("cmake@3.14:", type="build")

    depends_on("cuda", when="+cuda")
    depends_on("hip", when="+rocm")

    conflicts("~lld", when="+hip", msg="lld is needed for HIP plugin on AMD")
    conflicts("~lld", when=(sys.platform == "windows"), msg="lld is needed on Windows")

    root_cmakelists_dir = "llvm"
    build_targets = ["deploy-sycl-toolchain"]

    def cmake_args(self):
        spec = self.spec

        llvm_external_projects = "sycl;llvm-spirv;opencl;xpti;xptifw"
        libclc_amd_target_names = ";amdgcn;amdgcn--amdhsa"
        libclc_nvidia_target_names = ";nvptx64--;nvptx64--nvidiacl"

        if spec.platform != "darwin":
            llvm_external_projects += ";libdevice"

        if "+fusion" in spec:
            llvm_external_projects += ";sycl-fusion"

        sycl_dir = os.path.join(self.stage.source_path, "sycl")
        spirv_dir = os.path.join(self.stage.source_path, "llvm-spirv")
        xpti_dir = os.path.join(self.stage.source_path, "xpti")
        xptifw_dir = os.path.join(self.stage.source_path, "xptifw")
        libdevice_dir = os.path.join(self.stage.source_path, "libdevice")
        fusion_dir = os.path.join(self.stage.source_path, "sycl-fusion")
        llvm_enable_projects = "clang;" + llvm_external_projects
        libclc_targets_to_build = ""
        libclc_gen_remangled_variants = "OFF"
        sycl_enabled_plugins = "opencl"
        llvm_targets_to_build = get_llvm_targets_to_build(spec.target.family)

        if spec.platform != "darwin":
            sycl_enabled_plugins += ";level_zero"

        if "+lld" in spec:
            llvm_enable_projects += ";lld"

        if "+esimd-emulator" in spec:
            sycl_enabled_plugins += ";esimd_emulator"

        if "+cuda" in spec or "+rocm" in spec:
            llvm_enable_projects += ";libclc"
            libclc_gen_remangled_variants = "ON"

        if "+cuda" in spec:
            llvm_targets_to_build += ";NVPTX"
            libclc_targets_to_build = libclc_nvidia_target_names
            sycl_enabled_plugins += ";cuda"

        if "+rocm" in spec:
            llvm_targets_to_build += ";AMDGPU"
            libclc_targets_to_build += libclc_amd_target_names
            sycl_enabled_plugins += ";hip"

        if "+llvm-external-projects" in spec:
            llvm_external_projects += ";" + spec.variants["llvm-external-projects"].value.replace(
                ",", ";"
            )

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
            self.define("LIBCLC_GENERATE_REMANGLED_VARIANTS", libclc_gen_remangled_variants),
            self.define("SYCL_BUILD_PI_HIP_PLATFORM", "AMD"),
            self.define("LLVM_BUILD_TOOLS", "ON"),
            self.define_from_variant("SYCL_ENABLE_WERROR", "werror"),
            self.define("SYCL_INCLUDE_TESTS", "ON"),
            self.define_from_variant("LLVM_ENABLE_DOXYGEN", "docs"),
            self.define_from_variant("LLVM_ENABLE_SPHINX", "docs"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared-libs"),
            self.define("SYCL_ENABLE_XPTI_TRACING", "ON"),
            self.define_from_variant("LLVM_ENABLE_LLD", "lld"),
            self.define_from_variant("XPTI_ENABLE_WERROR", "werror"),
            self.define("SYCL_ENABLE_PLUGINS", sycl_enabled_plugins),
            self.define_from_variant("SYCL_ENABLE_KERNEL_FUSION", "fusion"),
            self.define_from_variant("EXTRA_SECURITY_FLAGS", "security_flags"),
        ]

        if "+cuda" in spec:
            args.append(self.define("CUDA_TOOLKIT_ROOT_DIR", spec["cuda"].prefix))

        if "+rocm" in spec:
            args.append(self.define("SYCL_BUILD_PI_HIP_ROCM_DIR", spec["hip"].prefix))

        return args

    def setup_build_environment(self, env):
        spec = self.spec
        if "+cuda" in spec:
            env.set("CUDA_LIB_PATH", "{0}/lib64/stubs".format(spec["cuda"].prefix))

    @property
    def cc(self):
        spec = self.spec
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert spec.concrete, msg
        if spec.external:
            return spec.extra_attributes["compilers"].get("c", None)
        result = None
        if "+clang" in spec:
            result = os.path.join(spec.prefix.bin, "clang")
        return result

    @property
    def cxx(self):
        spec = self.spec
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert spec.concrete, msg
        if spec.external:
            return spec.extra_attributes["compilers"].get("cxx", None)
        result = None
        if "+clang" in spec:
            result = os.path.join(spec.prefix.bin, "clang++")
        return result

    @run_after("install")
    def post_install(self):
        spec = self.spec
        clang_cpp_path = os.path.join(spec.prefix.bin, "clang++")
        dpcpp_path = os.path.join(spec.prefix.bin, "dpcpp")

        real_clang_cpp_path = os.path.realpath(clang_cpp_path)
        os.symlink(real_clang_cpp_path, dpcpp_path)

    def setup_run_environment(self, env):
        spec = self.spec
        env.set("CC", join_path(spec.prefix.bin, "clang"))
        env.set("CXX", join_path(spec.prefix.bin, "clang++"))
        env.prepend_path("LD_LIBRARY_PATH", join_path(spec.prefix, "lib"))


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
