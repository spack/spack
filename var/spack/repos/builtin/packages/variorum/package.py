# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import archspec

from spack.package import *


class Variorum(CMakePackage, CudaPackage, ROCmPackage):
    """Variorum is a library providing vendor-neutral interfaces for
    monitoring and controlling underlying hardware features.
    """

    homepage = "https://variorum.readthedocs.io"
    git = "https://github.com/llnl/variorum.git"
    url = "https://github.com/llnl/variorum/archive/v0.1.0.tar.gz"

    maintainers("slabasan", "rountree")

    version("dev", branch="dev")
    version("0.7.0", sha256="36ec0219379ea2b7c8f9770b3271335c776ff5a3de71585714c33356345b2f0c")
    version("0.6.0", sha256="c0928a0e6901808ee50142d1034de15edc2c90d7d1b9fbce43757226e7c04306")
    version("0.5.0", sha256="de331762e7945ee882d08454ff9c66436e2b6f87f761d2b31c6ab3028723bfed")
    version("0.4.1", sha256="be7407b856bc2239ecaa27d3df80aee2f541bb721fbfa183612bd9c0ce061f28")
    version("0.4.0", sha256="70ff1c5a3ae15d0bd07d409ab6f3c128e69528703a829cb18ecb4a50adeaea34")
    version("0.3.0", sha256="f79563f09b8fe796283c879b05f7730c36d79ca0346c12995b7bccc823653f42")
    version("0.2.0", sha256="b8c010b26aad8acc75d146c4461532cf5d9d3d24d6fc30ee68f6330a68e65744")
    version("0.1.0", tag="v0.1.0", commit="7747ee48cc60567bb3f09e732f24c041ecac894d")

    ############
    # Variants #
    ############
    variant("shared", default=True, description="Build Variorum as shared lib")
    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo"),
    )
    #intel gpu not supported in spack
    #variant("intel_gpu", default=False, description="Build for Intel GPU architecture")

    for cuda_val in CudaPackage.cuda_arch_values:
        print("RRR", cuda_val)
        if cuda_val != "70":
            print(cuda_val)
            conflicts(f"cuda_arch={cuda_val}", when="+cuda")

    #for rocm_val in ROCmPackage.amdgpu_targets:
    #    if rocm_val != "gfx906" or rocm_val != "gfx906:xnack-":
    #        conflicts(f"amdgpu_target={rocm_val}")

    ########################
    # Package dependencies #
    ########################
    depends_on("cmake@2.8:", type="build")
    depends_on("hwloc")
    depends_on("jansson", type="link")
    depends_on("cuda", when="+cuda_arch")
    depends_on("rocm-smi-lib", when="+rocm")

    root_cmakelists_dir = "src"

    def cmake_args(self):
        spec = self.spec
        cmake_args = []

        cmake_args.append("-DJANSSON_DIR={0}".format(spec["jansson"].prefix))
        cmake_args.append("-DHWLOC_DIR={0}".format(spec["hwloc"].prefix))
        cmake_args.append("-DBUILD_DOCS=OFF")

        if spec.satisfies("%cce"):
            cmake_args.append("-DCMAKE_C_FLAGS=-fcommon")
            cmake_args.append("-DCMAKE_CCC_FLAGS=-fcommon")
            cmake_args.append("-DCMAKE_Fortran_FLAGS=-ef")

        if "+shared" in spec:
            cmake_args.append("-DBUILD_SHARED_LIBS=ON")
        else:
            cmake_args.append("-DBUILD_SHARED_LIBS=OFF")

        # should only be building for AMD or NVIDIA GPU architecture
        if "+cuda" in spec:
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=ON")
        elif "+rocm" in spec:
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=ON")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=OFF")

        if "build_type=Debug" in spec:
            cmake_args.append("-DVARIORUM_DEBUG=ON")
        else:
            cmake_args.append("-DVARIORUM_DEBUG=OFF")

        if self.run_tests:
            cmake_args.append("-DBUILD_TESTS=ON")
        else:
            cmake_args.append("-DBUILD_TESTS=OFF")

        cpu_uarch = spec.target.microarchitecture
        cpu_vendor = archspec.cpu.host().to_dict()["vendor"]

        #taken from list of archspec.cpu.TARGETS
        supported_amd_targets = ["zen2"]
        supported_arm_targets = ["neoverse_n1"]
        supported_ibm_targets = ["power9le"]
        supported_intel_targets = [
            "sandybridge",
            "ivybridge",
            "haswell",
            "broadwell",
            "skylake",
            "cascadelake",
            "icelake",
        ]

        if cpu_vendor == "AuthenticAMD" and cpu_uarch in supported_amd_targets:
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=ON")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=OFF")
        elif cpu_vendor == "ARM" and cpu_uarch in supported_arm_targets:
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=ON")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=OFF")
        elif cpu_vendor == "IBM" and cpu_uarch in supported_ibm_targets:
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=ON")
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=OFF")
        elif cpu_vendor == "GenuineIntel" and cpu_uarch in supported_intel_targets:
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=ON")
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=OFF")
        #else:
        #    raise TypeError("unsupported architecture")

        return cmake_args
