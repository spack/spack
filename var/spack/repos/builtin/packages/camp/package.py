# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import glob
import re

from spack.package import *


def spec_uses_toolchain(spec):
    gcc_toolchain_regex = re.compile(".*gcc-toolchain.*")
    using_toolchain = list(filter(gcc_toolchain_regex.match, spec.compiler_flags["cxxflags"]))
    return using_toolchain

def spec_uses_gccname(spec):
    gcc_name_regex = re.compile(".*gcc-name.*")
    using_gcc_name = list(filter(gcc_name_regex.match, spec.compiler_flags["cxxflags"]))
    return using_gcc_name

def hip_repair_options(options, spec):
    # there is only one dir like this, but the version component is unknown
    options.append(
        "-DHIP_CLANG_INCLUDE_PATH="
        + glob.glob("{}/lib/clang/*/include".format(spec["llvm-amdgpu"].prefix))[0]
    )

def hip_repair_cache(options, spec):
    # there is only one dir like this, but the version component is unknown
    options.append(
        cmake_cache_path(
            "HIP_CLANG_INCLUDE_PATH",
            glob.glob("{}/lib/clang/*/include".format(spec["llvm-amdgpu"].prefix))[0],
        )
    )

def hip_for_radiuss_projects(options, spec, compiler):
    # Here is what is typically needed for radiuss projects when building with rocm
    hip_root = spec["hip"].prefix
    rocm_root = hip_root + "/.."
    options.append(cmake_cache_path("HIP_ROOT_DIR", hip_root))
    options.append(cmake_cache_path("ROCM_ROOT_DIR", rocm_root))

    hip_repair_cache(options, spec)

    archs = spec.variants["amdgpu_target"].value
    if archs != "none":
        arch_str = ",".join(archs)
        options.append(
            cmake_cache_string("HIP_HIPCC_FLAGS", "--amdgpu-target={0}".format(arch_str))
        )
        options.append(
            cmake_cache_string("CMAKE_HIP_ARCHITECTURES", arch_str)
        )

    # adrienbernede-22-11:
    #   Specific to Umpire, attempt port to RAJA and CHAI
    hip_link_flags = ""
    if "%gcc" in spec or spec_uses_toolchain(spec):
        if "%gcc" in spec:
            gcc_bin = os.path.dirname(compiler.cxx)
            gcc_prefix = os.path.join(gcc_bin, "..")
        else:
            gcc_prefix = spec_uses_toolchain(spec)[0]
        options.append(cmake_cache_string("HIP_CLANG_FLAGS", "--gcc-toolchain={0}".format(gcc_prefix)))
        options.append(cmake_cache_string("CMAKE_EXE_LINKER_FLAGS", hip_link_flags + " -Wl,-rpath {}/lib64".format(gcc_prefix)))
    else:
        options.append(cmake_cache_string("CMAKE_EXE_LINKER_FLAGS", "-Wl,-rpath={0}/llvm/lib/".format(rocm_root)))

def cuda_for_radiuss_projects(options, spec):
    # Here is what is typically needed for radiuss projects when building with cuda

    cuda_flags = []
    if not spec.satisfies("cuda_arch=none"):
        cuda_arch = spec.variants["cuda_arch"].value
        cuda_flags.append("-arch sm_{0}".format(cuda_arch[0]))
        options.append(
            cmake_cache_string("CUDA_ARCH", "sm_{0}".format(cuda_arch[0])))
        options.append(
            cmake_cache_string("CMAKE_CUDA_ARCHITECTURES", "{0}".format(cuda_arch[0])))
    if spec_uses_toolchain(spec):
        cuda_flags.append("-Xcompiler {}".format(spec_uses_toolchain(spec)[0]))
    if (spec.satisfies("%gcc@8.1: target=ppc64le")):
        cuda_flags.append("-Xcompiler -mno-float128")
    options.append(cmake_cache_string("CMAKE_CUDA_FLAGS", " ".join(cuda_flags)))

def blt_link_helpers(options, spec, compiler):
    ### From local package:
    if compiler.fc:
        fortran_compilers = ["gfortran", "xlf"]
        if any(f_comp in compiler.fc for f_comp in fortran_compilers) and ("clang" in compiler.cxx):
            # Pass fortran compiler lib as rpath to find missing libstdc++
            libdir = os.path.join(os.path.dirname(
                           os.path.dirname(compiler.fc)), "lib")
            flags = ""
            for _libpath in [libdir, libdir + "64"]:
                if os.path.exists(_libpath):
                    flags += " -Wl,-rpath,{0}".format(_libpath)
            description = ("Adds a missing libstdc++ rpath")
            if flags:
                options.append(cmake_cache_string("BLT_EXE_LINKER_FLAGS", flags, description))

            # Ignore conflicting default gcc toolchain
            options.append(cmake_cache_string("BLT_CMAKE_IMPLICIT_LINK_DIRECTORIES_EXCLUDE",
            "/usr/tce/packages/gcc/gcc-4.9.3/lib64;/usr/tce/packages/gcc/gcc-4.9.3/gnu/lib64/gcc/powerpc64le-unknown-linux-gnu/4.9.3;/usr/tce/packages/gcc/gcc-4.9.3/gnu/lib64;/usr/tce/packages/gcc/gcc-4.9.3/lib64/gcc/x86_64-unknown-linux-gnu/4.9.3"))

    compilers_using_toolchain = ["pgc++", "xlc++", "xlC_r", "icpc", "clang++", "icpx"]
    if any(tc_comp in compiler.cxx for tc_comp in compilers_using_toolchain):
        if spec_uses_toolchain(spec) or spec_uses_gccname(spec):

            # Ignore conflicting default gcc toolchain
            options.append(cmake_cache_string("BLT_CMAKE_IMPLICIT_LINK_DIRECTORIES_EXCLUDE",
            "/usr/tce/packages/gcc/gcc-4.9.3/lib64;/usr/tce/packages/gcc/gcc-4.9.3/gnu/lib64/gcc/powerpc64le-unknown-linux-gnu/4.9.3;/usr/tce/packages/gcc/gcc-4.9.3/gnu/lib64;/usr/tce/packages/gcc/gcc-4.9.3/lib64/gcc/x86_64-unknown-linux-gnu/4.9.3"))

    if "cce" in compiler.cxx:
        description = (
            "Adds a missing rpath for libraries " "associated with the fortran compiler"
        )
        # Here is where to find libs that work for fortran
        libdir = "/opt/cray/pe/cce/{0}/cce-clang/x86_64/lib".format(compiler.version)
        linker_flags = "${{BLT_EXE_LINKER_FLAGS}} -Wl,-rpath,{0}".format(libdir)

        version = "{0}".format(compiler.version)

        if version == "16.0.0":
            # Here is another directory added by cce@16.0.0
            libdir = os.path.join(libdir,"x86_64-unknown-linux-gnu")
            linker_flags += " -Wl,-rpath,{0}".format(libdir)

        options.append(cmake_cache_string("BLT_EXE_LINKER_FLAGS", linker_flags, description))


class Camp(CMakePackage, CudaPackage, ROCmPackage):
    """
    Compiler agnostic metaprogramming library providing concepts,
    type operations and tuples for C++ and cuda
    """

    homepage = "https://github.com/LLNL/camp"
    git = "https://github.com/LLNL/camp.git"
    url = "https://github.com/LLNL/camp/archive/v0.1.0.tar.gz"

    maintainers("trws")

    version("main", branch="main", submodules="False")
    version("2023.06.0", tag="v2023.06.0", submodules=False)
    version("2022.10.1", sha256="2d12f1a46f5a6d01880fc075cfbd332e2cf296816a7c1aa12d4ee5644d386f02")
    version("2022.10.0", sha256="3561c3ef00bbcb61fe3183c53d49b110e54910f47e7fc689ad9ccce57e55d6b8")
    version("2022.03.2", sha256="bc4aaeacfe8f2912e28f7a36fc731ab9e481bee15f2c6daf0cb208eed3f201eb")
    version("2022.03.0", sha256="e9090d5ee191ea3a8e36b47a8fe78f3ac95d51804f1d986d931e85b8f8dad721")
    version("0.3.0", sha256="129431a049ca5825443038ad5a37a86ba6d09b2618d5fe65d35f83136575afdb")
    version("0.2.3", sha256="58a0f3bd5eadb588d7dc83f3d050aff8c8db639fc89e8d6553f9ce34fc2421a7")
    version("0.2.2", sha256="194d38b57e50e3494482a7f94940b27f37a2bee8291f2574d64db342b981d819")
    version("0.1.0", sha256="fd4f0f2a60b82a12a1d9f943f8893dc6fe770db493f8fae5ef6f7d0c439bebcc")

    # TODO: figure out gtest dependency and then set this default True.
    variant("tests", default=False, description="Build tests")
    variant("openmp", default=False, description="Build with OpenMP support")

    depends_on("cub", when="+cuda")

    depends_on("blt")

    conflicts("^blt@:0.3.6", when="+rocm")

    def cmake_args(self):
        spec = self.spec

        options = []

        options.append("-DBLT_SOURCE_DIR={0}".format(spec["blt"].prefix))

        if "+cuda" in spec:
            options.extend([
                "-DENABLE_CUDA=ON",
                "-DCUDA_TOOLKIT_ROOT_DIR=%s" % (spec["cuda"].prefix)
            ])

            if not spec.satisfies("cuda_arch=none"):
                cuda_arch = spec.variants["cuda_arch"].value
                options.append("-DCMAKE_CUDA_ARCHITECTURES={0}".format(cuda_arch[0]))
                options.append("-DCUDA_ARCH=sm_{0}".format(cuda_arch[0]))
                flag = "-arch sm_{0}".format(cuda_arch[0])
                options.append("-DCMAKE_CUDA_FLAGS:STRING={0}".format(flag))
        else:
            options.append("-DENABLE_CUDA=OFF")

        if "+rocm" in spec:
            options.extend([
                "-DENABLE_HIP=ON",
                "-DHIP_ROOT_DIR={0}".format(spec["hip"].prefix)
            ])

            hip_repair_options(options, spec)

            archs = self.spec.variants["amdgpu_target"].value
            options.append("-DCMAKE_HIP_ARCHITECTURES={0}".format(archs))
            if archs != "none":
                arch_str = ",".join(archs)
                options.append("-DHIP_HIPCC_FLAGS=--amdgpu-target={0}".format(arch_str))
        else:
            options.append("-DENABLE_HIP=OFF")

        options.append(self.define_from_variant("ENABLE_OPENMP", "openmp"))
        options.append(self.define_from_variant("ENABLE_TESTS", "tests"))

        return options
