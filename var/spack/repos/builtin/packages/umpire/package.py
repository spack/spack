# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import socket
import re

import llnl.util.tty as tty

from spack.package import *
from .camp import hip_for_radiuss_projects
from .camp import cuda_for_radiuss_projects
from .camp import blt_link_helpers



class Umpire(CachedCMakePackage, CudaPackage, ROCmPackage):
    """An application-focused API for memory management on NUMA & GPU
    architectures"""

    homepage = "https://github.com/LLNL/Umpire"
    git = "https://github.com/LLNL/Umpire.git"
    tags = ["radiuss", "e4s"]

    maintainers("davidbeckingsale")

    version("develop", branch="develop", submodules=False)
    version("main", branch="main", submodules=False)
    version("2023.06.0", tag="v2023.06.0", submodules=False)
    version("2022.10.0", tag="v2022.10.0", submodules=False)
    version("2022.03.1", tag="v2022.03.1", submodules=False)
    version("2022.03.0", tag="v2022.03.0", submodules=False)
    version("6.0.0", tag="v6.0.0", submodules=True)
    version("5.0.1", tag="v5.0.1", submodules=True)
    version("5.0.0", tag="v5.0.0", submodules=True)
    version("4.1.2", tag="v4.1.2", submodules=True)
    version("4.1.1", tag="v4.1.1", submodules=True)
    version("4.1.0", tag="v4.1.0", submodules=True)
    version("4.0.1", tag="v4.0.1", submodules=True)
    version("4.0.0", tag="v4.0.0", submodules=True)
    version("3.0.0", tag="v3.0.0", submodules=True)
    version("2.1.0", tag="v2.1.0", submodules=True)
    version("2.0.0", tag="v2.0.0", submodules=True)
    version("1.1.0", tag="v1.1.0", submodules=True)
    version("1.0.1", tag="v1.0.1", submodules=True)
    version("1.0.0", tag="v1.0.0", submodules=True)
    version("0.3.5", tag="v0.3.5", submodules=True)
    version("0.3.4", tag="v0.3.4", submodules=True)
    version("0.3.3", tag="v0.3.3", submodules=True)
    version("0.3.2", tag="v0.3.2", submodules=True)
    version("0.3.1", tag="v0.3.1", submodules=True)
    version("0.3.0", tag="v0.3.0", submodules=True)
    version("0.2.4", tag="v0.2.4", submodules=True)
    version("0.2.3", tag="v0.2.3", submodules=True)
    version("0.2.2", tag="v0.2.2", submodules=True)
    version("0.2.1", tag="v0.2.1", submodules=True)
    version("0.2.0", tag="v0.2.0", submodules=True)
    version("0.1.4", tag="v0.1.4", submodules=True)
    version("0.1.3", tag="v0.1.3", submodules=True)

    patch("export_includes.patch", when="@2022.10.0")
    patch("std-filesystem-pr784.patch", when="@2022.03.1 +rocm ^blt@0.5.2:")
    patch("camp_target_umpire_3.0.0.patch", when="@3.0.0")
    patch("cmake_version_check.patch", when="@4.1")
    patch("missing_header_for_numeric_limits.patch", when="@4.1:5.0.1")

    # export targets when building pre-6.0.0 release with BLT 0.4.0+
    patch(
        "https://github.com/LLNL/Umpire/commit/5773ce9af88952c8d23f9bcdcb2e503ceda40763.patch?full_index=1",
        sha256="f3b21335ce5cf9c0fecc852a94dfec90fb5703032ac97f9fee104af9408d8899",
        when="@:5.0.1 ^blt@0.4:",
    )

    variant("fortran", default=False, description="Build C/Fortran API")
    variant("c", default=True, description="Build C API")
    variant("mpi", default=False, description="Enable MPI support")
    variant("ipc_shmem", default=False, description="Enable POSIX shared memory")
    variant("sqlite_experimental", default=False, description="Enable sqlite integration with umpire events (Experimental)")
    variant("numa", default=False, description="Enable NUMA support")
    variant("shared", default=True, description="Enable Shared libs")
    variant("openmp", default=False, description="Build with OpenMP support")
    variant("openmp_target", default=False, description="Build with OpenMP 4.5 support")
    variant("deviceconst", default=False, description="Enables support for constant device memory")
    variant("examples", default=False, description="Build Umpire Examples")
    variant(
        "tests",
        default="none",
        values=("none", "basic", "benchmarks"),
        multi=False,
        description="Tests to run",
    )
    variant("tools", default=False, description="Enable tools")
    variant("backtrace", default=False, description="Enable backtrace tools")
    variant("dev_benchmarks", default=False, description="Enable Developer Benchmarks")
    variant("device_alloc", default=False, description="Enable DeviceAllocator")
    variant("werror", default=True, description="Enable warnings as errors")
    variant("asan", default=False, description="Enable ASAN")
    variant("sanitizer_tests", default=False, description="Enable address sanitizer tests")

    depends_on("cmake@3.8:", type="build")
    depends_on("cmake@3.9:", when="+cuda", type="build")
    depends_on("cmake@3.20:", when="@2022.10.0:", type="build")
    depends_on("cmake@3.23:", when="@2022.10.0: +rocm", type="build")
    depends_on("cmake@3.14:", when="@2022.03.0:", type="build")
    depends_on("cmake@:3.20", when="@2022.03.0:2022.03 +rocm", type="build")

    depends_on("blt@develop", type="build", when="@develop")
    depends_on("blt@0.5.3:", type="build", when="@2023.06.0:")
    depends_on("blt@0.5.2:", type="build", when="@2022.10.0:")
    depends_on("blt@0.5.0:", type="build", when="@2022.03.0:")
    depends_on("blt@0.4.1", type="build", when="@6.0.0")
    depends_on("blt@0.4.0:", type="build", when="@4.1.3:5.0.1")
    depends_on("blt@0.3.6:", type="build", when="@:4.1.2")
    conflicts("^blt@:0.3.6", when="+rocm")

    depends_on("camp", when="@5.0.0:")
    depends_on("camp@0.2.2:0.2.3", when="@6.0.0")
    depends_on("camp@0.1.0", when="@5.0.0:5.0.1")
    depends_on("camp@2023.06", when="@2023.06")
    depends_on("camp@2022.03.2:", when="@2022.03.0:")
    depends_on("camp@2022.10.0:", when="@2022.10.0:")
    depends_on("camp@2023.06.0:", when="@2023.06.0:")
    depends_on("camp@main", when="@main")
    depends_on("camp@main", when="@develop")
    depends_on("camp+openmp", when="+openmp")
    depends_on("camp~cuda", when="~cuda")

    depends_on("sqlite", when="+sqlite_experimental")
    depends_on("mpi", when="+mpi")

    with when("@5.0.0:"):
        with when("+cuda"):
            depends_on("camp+cuda")
            for sm_ in CudaPackage.cuda_arch_values:
                depends_on("camp+cuda cuda_arch={0}".format(sm_), when="cuda_arch={0}".format(sm_))

        with when("+rocm"):
            depends_on("camp+rocm")
            for arch_ in ROCmPackage.amdgpu_targets:
                depends_on(
                    "camp+rocm amdgpu_target={0}".format(arch_),
                    when="amdgpu_target={0}".format(arch_),
                )

    conflicts("+numa", when="@:0.3.2")
    conflicts("~c", when="+fortran", msg="Fortran API requires C API")

    # device allocator must be used with more current umpire versions, rocm 5.4.0 and greater,
    # and with either rocm or cuda enabled
    conflicts("+device_alloc", when="@:2022.03.0")
    conflicts("+device_alloc", when="^hip@:5.3.99")
    conflicts("+device_alloc", when="~rocm~cuda")

    conflicts("+deviceconst", when="~rocm~cuda")
    conflicts("~openmp", when="+openmp_target", msg="OpenMP target requires OpenMP")
    conflicts("+cuda", when="+rocm")
    conflicts("+tools", when="+rocm")
    conflicts("+rocm", when="+openmp_target", msg="Cant support both rocm and openmp device backends at once")
    conflicts("~mpi", when="+ipc_shmem", msg="Shared Memory Allocator requires MPI")
    conflicts("+ipc_shmem", when="@:5.0.1")

    conflicts("+sqlite_experimental", when="@:6.0.0")
    conflicts("+sanitizer_tests", when="~asan")

    # device allocator exports device code, which requires static libs
    # currently only available for cuda.
    conflicts("+shared", when="+cuda")

    # https://github.com/LLNL/Umpire/issues/653
    # This range looks weird, but it ensures the concretizer looks at it as a
    # range, not as a concrete version, so that it also matches 10.3.* versions.
    conflicts("%gcc@10.3.0:10.3", when="+cuda")

    def _get_sys_type(self, spec):
        sys_type = spec.architecture
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        return sys_type

    @property
    def cache_name(self):
        hostname = socket.gethostname()
        if "SYS_TYPE" in env:
            hostname = hostname.rstrip("1234567890")
        return "{0}-{1}-{2}@{3}-{4}.cmake".format(
            hostname,
            self._get_sys_type(self.spec),
            self.spec.compiler.name,
            self.spec.compiler.version,
            self.spec.dag_hash(8)
        )

    def initconfig_compiler_entries(self):
        spec = self.spec
        compiler = self.compiler
        # Default entries are already defined in CachedCMakePackage, inherit them:
        entries = super().initconfig_compiler_entries()



        # adrienbernede-22-11:
        #   This was in upstream Spack raja package, but it’s causing the follwing failure:
        #     CMake Error in src/umpire/CMakeLists.txt:
        #     No known features for CXX compiler
        #
        #if "+rocm" in spec:
        #    entries.insert(0, cmake_cache_path("CMAKE_CXX_COMPILER", spec["hip"].hipcc))

        option_prefix = "UMPIRE_" if spec.satisfies("@2022.03.0:") else ""

        if "+fortran" in spec and compiler.fc is not None:
            entries.append(cmake_cache_option("ENABLE_FORTRAN", True))
        else:
            entries.append(cmake_cache_option("ENABLE_FORTRAN", False))

        entries.append(cmake_cache_option("{}ENABLE_C".format(option_prefix), "+c" in spec))

        blt_link_helpers(entries, spec, compiler)

        #adrienbernede-22-11:
        #  Specific to Umpire local package, worth sharing?
        entries = [x for x in entries if not "COMPILER_ID" in x]

        return entries

    def initconfig_hardware_entries(self):
        spec = self.spec
        compiler = self.compiler
        entries = super().initconfig_hardware_entries()

        option_prefix = "UMPIRE_" if spec.satisfies("@2022.03.0:") else ""

        if "+cuda" in spec:
            entries.append(cmake_cache_option("ENABLE_CUDA", True))
            cuda_for_radiuss_projects(entries, spec)
        else:
            entries.append(cmake_cache_option("ENABLE_CUDA", False))

        if "+rocm" in spec:
            entries.append(cmake_cache_option("ENABLE_HIP", True))
            hip_for_radiuss_projects(entries, spec, compiler)
        else:
            entries.append(cmake_cache_option("ENABLE_HIP", False))

        entries.append(cmake_cache_option(
            "{}ENABLE_DEVICE_CONST".format(option_prefix), "+deviceconst" in spec))

        entries.append(cmake_cache_option(
            "{}ENABLE_OPENMP_TARGET".format(option_prefix), "+openmp_target" in spec))
        if "+openmp_target" in spec and "%xl" in spec:
                entries.append(cmake_cache_string("OpenMP_CXX_FLAGS", "-qsmp;-qoffload"))

        return entries

    def initconfig_mpi_entries(self):
        spec = self.spec

        entries = super(Umpire, self).initconfig_mpi_entries()
        entries.append(cmake_cache_option("ENABLE_MPI", "+mpi" in spec))

        return entries

    def initconfig_package_entries(self):
        spec = self.spec
        entries = []

        option_prefix = "UMPIRE_" if spec.satisfies("@2022.03.0:") else ""

        # TPL locations
        entries.append("#------------------{0}".format("-" * 60))
        entries.append("# TPLs")
        entries.append("#------------------{0}\n".format("-" * 60))

        entries.append(cmake_cache_path("BLT_SOURCE_DIR", spec["blt"].prefix))
        if spec.satisfies("@5.0.0:"):
            entries.append(cmake_cache_path("camp_DIR", spec["camp"].prefix))

        # Build options
        entries.append("#------------------{0}".format("-" * 60))
        entries.append("# Build Options")
        entries.append("#------------------{0}\n".format("-" * 60))

        entries.append(cmake_cache_string(
            "CMAKE_BUILD_TYPE", spec.variants["build_type"].value))
        entries.append(cmake_cache_option(
            "BUILD_SHARED_LIBS", "+shared" in spec))
        entries.append(cmake_cache_option(
            "ENABLE_WARNINGS_AS_ERRORS", "+werror" in spec))

        # Generic options that have a prefixed equivalent in Umpire CMake
        entries.append(cmake_cache_option(
            "ENABLE_OPENMP", "+openmp" in spec))
        entries.append(cmake_cache_option(
            "ENABLE_EXAMPLES", "+examples" in spec))
        entries.append(cmake_cache_option(
            "ENABLE_DOCS", False))
        if "tests=benchmarks" in spec or "+dev_benchmarks" in spec:
            # BLT requires ENABLE_TESTS=True to enable benchmarks
            entries.append(cmake_cache_option(
                "ENABLE_BENCHMARKS", True))
            entries.append(cmake_cache_option(
                "ENABLE_TESTS", True))
        else:
            entries.append(cmake_cache_option(
                "ENABLE_BENCHMARKS", False))
            entries.append(cmake_cache_option(
                "ENABLE_TESTS", "tests=none" not in spec))

        # Prefixed options that used to be name without one
        entries.append(cmake_cache_option(
            "{}ENABLE_NUMA".format(option_prefix), "+numa" in spec))
        entries.append(cmake_cache_option(
            "{}ENABLE_DEVELOPER_BENCHMARKS".format(option_prefix), "+dev_benchmarks" in spec))
        entries.append(cmake_cache_option(
            "{}ENABLE_TOOLS".format(option_prefix), "+tools" in spec))
        entries.append(cmake_cache_option(
            "{}ENABLE_BACKTRACE".format(option_prefix), "+backtrace" in spec))
        entries.append(cmake_cache_option(
            "{}ENABLE_ASAN".format(option_prefix), "+asan" in spec))
        entries.append(cmake_cache_option(
            "{}ENABLE_SANITIZER_TESTS".format(option_prefix), "+sanitizer_tests" in spec))

        # Recent options, were never name without prefix
        entries.append(cmake_cache_option(
            "UMPIRE_ENABLE_DEVICE_ALLOCATOR", "+device_alloc" in spec))
        entries.append(cmake_cache_option(
            "UMPIRE_ENABLE_SQLITE_EXPERIMENTAL", "+sqlite_experimental" in spec))
        if "+sqlite_experimental" in spec:
            entries.append(cmake_cache_path(
                "SQLite3_ROOT" ,spec["sqlite"].prefix))

        # This option was renamed later than the others
        if spec.satisfies("@2022.10.0:"):
            entries.append(cmake_cache_option(
                "UMPIRE_ENABLE_IPC_SHARED_MEMORY", "+ipc_shmem" in spec))
        else:
            entries.append(cmake_cache_option(
                "ENABLE_IPC_SHARED_MEMORY", "+ipc_shmem" in spec))

        return entries

    def cmake_args(self):
        options = []
        return options

    def test(self):
        """Perform stand-alone checks on the installed package."""
        if self.spec.satisfies("@:1") or not os.path.isdir(self.prefix.bin):
            tty.info("Skipping: checks not installed in bin for v{0}".format(self.version))
            return

        # Run a subset of examples PROVIDED installed
        # tutorials with readily checkable outputs.
        checks = {
            "malloc": ["99 should be 99"],
            "recipe_dynamic_pool_heuristic": ["in the pool", "releas"],
            "recipe_no_introspection": ["has allocated", "used"],
            "strategy_example": ["Available allocators", "HOST"],
            "tut_copy": ["Copied source data"],
            "tut_introspection": ["Allocator used is HOST", "size of the allocation"],
            "tut_memset": ["Set data from HOST"],
            "tut_move": ["Moved source data", "HOST"],
            "tut_reallocate": ["Reallocated data"],
            "vector_allocator": [""],
        }

        for exe in checks:
            expected = checks[exe]
            reason = "test: checking output from {0}".format(exe)
            self.run_test(
                exe,
                [],
                expected,
                0,
                installed=False,
                purpose=reason,
                skip_missing=True,
                work_dir=self.prefix.bin,
            )
