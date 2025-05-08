# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Variorum(CMakePackage):
    """Variorum is a library providing vendor-neutral interfaces for
    monitoring and controlling underlying hardware features.
    """

    homepage = "https://variorum.readthedocs.io"
    git = "https://github.com/llnl/variorum.git"
    url = "https://github.com/llnl/variorum/archive/v0.8.0.tar.gz"

    maintainers("slabasan", "rountree")

    tags = ["e4s"]

    license("MIT")

    version("dev", branch="dev")
    version("0.8.0", sha256="0e7288d523488b2a585af8ffeb7874721526f46df563b21fc51e8846bf65f7d8")

    ############
    # Variants #
    ############
    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release"),
    )
    variant( "cpu", default="Intel", description="Supported CPU architecture",
        values=("Intel", "INTEL", "intel", "AMD", "amd", "IBM", "ibm", "ARM", "arm"), multi=False )
    variant( "gpu", default="none", description="Supported GPU architecture",
        values=("Intel", "INTEL", "intel", "AMD", "amd", "NVIDIA", "nvidia", "none" ), multi=False )

    ########################
    # Package dependencies #
    ########################
    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake@2.8:", type="build")
    depends_on("hwloc")
    depends_on("jansson", type="link")

    root_cmakelists_dir = "src"

    def cmake_args(self):
        spec = self.spec
        cmake_args = []

        cmake_args.append("-DJANSSON_DIR={0}".format(spec["jansson"].prefix))

        if spec.satisfies("%cce"):
            cmake_args.append("-DCMAKE_C_FLAGS=-fcommon")
            cmake_args.append("-DCMAKE_CCC_FLAGS=-fcommon")
            cmake_args.append("-DCMAKE_Fortran_FLAGS=-ef")

        # CPU architecture selection.
        if "cpu=Intel" or "cpu=INTEL" or "cpu=intel" in spec:
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=ON")
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=OFF")
        elif "cpu=AMD" or "cpu=amd" in spec:
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=ON")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=OFF")
        elif "cpu=IBM" or "cpu=ibm" in spec:
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=ON")
        elif "cpu=ARM" or "cpu=arm" in spec:
            cmake_args.append("-DVARIORUM_WITH_INTEL_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_AMD_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_IBM_CPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_ARM_CPU=ON")

        # GPU architecture selection.
        if "gpu=Intel" or "gpu=INTEL" or "gpu=intel" in spec:
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=ON")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=OFF")
        elif "gpu=AMD" or "gpu=amd" in spec:
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=ON")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=OFF")
        elif "gpu=NVIDIA" or "gpu=nvidia" in spec:
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=ON")
        else:
            cmake_args.append("-DVARIORUM_WITH_INTEL_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_AMD_GPU=OFF")
            cmake_args.append("-DVARIORUM_WITH_NVIDIA_GPU=OFF")

        if "build_type=Debug" in spec:
            cmake_args.append("-DVARIORUM_DEBUG=ON")
        else:
            cmake_args.append("-DVARIORUM_DEBUG=OFF")

        if self.run_tests:
            cmake_args.append("-DBUILD_TESTS=ON")
        else:
            cmake_args.append("-DBUILD_TESTS=OFF")

        return cmake_args
