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
    # intel gpu not supported in spack
    # variant("intel_gpu", default=False, description="Build for Intel GPU architecture")

    ########################
    # Package dependencies #
    ########################
    depends_on("cmake@2.8:", type="build")
    depends_on("hwloc")
    depends_on("jansson", type="link")
    depends_on("cuda", when="+cuda")
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

        if "build_type=Debug" in spec:
            cmake_args.append("-DVARIORUM_DEBUG=ON")
        else:
            cmake_args.append("-DVARIORUM_DEBUG=OFF")

        if self.run_tests:
            cmake_args.append("-DBUILD_TESTS=ON")
        else:
            cmake_args.append("-DBUILD_TESTS=OFF")

        target = self.spec.target
        cpu_vendor = target.microarchitecture.vendor

        # taken from list of archspec.cpu.TARGETS
        supported_amd_cpu_targets = ["zen2"]
        supported_arm_cpu_targets = ["neoverse_n1"]
        supported_ibm_cpu_targets = ["power9le"]
        supported_intel_cpu_targets = [
            "sandybridge",
            "ivybridge",
            "haswell",
            "broadwell",
            "skylake",
            "cascadelake",
            "icelake",
        ]
        supported_nvidia_gpu_targets = [70]
        supported_amd_gpu_targets = ["gfx906", "gfx906:xnack-"]

        for arch in archspec.cpu.TARGETS:
            if (
                arch
                not in supported_amd_cpu_targets
                + supported_arm_cpu_targets
                + supported_ibm_cpu_targets
                + supported_intel_cpu_targets
            ):
                conflicts(f"target={arch}", when="~cuda~rocm")

        for arch in ROCmPackage.amdgpu_targets:
            if arch not in supported_amd_gpu_targets:
                conflicts(f"amdgpu_target={arch}", when="+rocm")

        for arch in CudaPackage.cuda_arch_values:
            if arch not in supported_nvidia_gpu_targets:
                conflicts(f"cuda_arch={arch}", when="+cuda")

        if cpu_vendor == "AuthenticAMD":
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=ON")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=OFF")
        elif cpu_vendor == "ARM":
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=ON")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=OFF")
        elif cpu_vendor == "IBM":
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=ON")
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=OFF")
        elif cpu_vendor == "GenuineIntel":
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=ON")
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=OFF")
        elif "+cuda" in spec:
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=ON")
            cmake_args.append("-DNVML_DIR={0}".format(spec["cuda"].prefix))
            cmake_args.append(
                "-DCMAKE_SHARED_LINKER_FLAGS=-L{0}/nvidia/targets/ppc64le-linux/lib/stubs/ -lnvidia-ml".format(
                    spec["cuda"].prefix
                )
            )
        elif "+rocm" in spec:
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=ON")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=OFF")
            cmake_args.append("-DROCM_DIR={0}".format(spec["hip"].prefix))
            cmake_args.append(
                "-DCMAKE_SHARED_LINKER_FLAGS=-L{0}/lib -lrocm_smi64".format(spec["hip"].prefix)
            )
        else:
            raise TypeError("Building on unsupported architecture")

        return cmake_args
