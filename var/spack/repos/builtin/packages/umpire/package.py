# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import socket

import llnl.util.tty as tty

from spack.package import *
from spack.pkg.builtin.camp import hip_repair_cache


class Umpire(CachedCMakePackage, CudaPackage, ROCmPackage):
    """An application-focused API for memory management on NUMA & GPU
    architectures"""

    homepage = "https://github.com/LLNL/Umpire"
    git = "https://github.com/LLNL/Umpire.git"
    tags = ["radiuss", "e4s"]

    maintainers("davidbeckingsale")

    version("develop", branch="develop", submodules=False)
    version("main", branch="main", submodules=False)
    version(
        "2022.10.0",
        tag="v2022.10.0",
        commit="93b1441aaa258c1dcd211a552b75cff6461a2a8a",
        submodules=False,
    )
    version(
        "2022.03.1",
        tag="v2022.03.1",
        commit="6bf231bdbbc797df70d60027ddb714ac2ef7c0a1",
        submodules=False,
    )
    version(
        "2022.03.0",
        tag="v2022.03.0",
        commit="2db6224ae0c3f3e0bbd6722e95c1167b7f79be7b",
        submodules=False,
    )
    version(
        "6.0.0", tag="v6.0.0", commit="5f886b4299496b7cb6f9d62dc1372ce6d3832fbc", submodules=True
    )
    version(
        "5.0.1", tag="v5.0.1", commit="5201a47a35e3844160dcbecd0916f8c96aa7dd07", submodules=True
    )
    version(
        "5.0.0", tag="v5.0.0", commit="2196615500057e068f2d93597b4f8da89d582afb", submodules=True
    )
    version(
        "4.1.2", tag="v4.1.2", commit="447f4640eff7b8f39d3c59404f3b03629b90c021", submodules=True
    )
    version(
        "4.1.1", tag="v4.1.1", commit="df1830b5ea04185f93fc229ed667da62d1d2d6e3", submodules=True
    )
    version(
        "4.1.0", tag="v4.1.0", commit="62f146d9c6b291cd79b29386dcb84b30f7b4212e", submodules=True
    )
    version(
        "4.0.1", tag="v4.0.1", commit="06d8692d084a88b15b0ef2794a1da779197da747", submodules=True
    )
    version(
        "4.0.0", tag="v4.0.0", commit="bdd598512516bdc4238502f180c8a7e145c6e68f", submodules=True
    )
    version(
        "3.0.0", tag="v3.0.0", commit="657676087574f61f9d90b996a3bdbf4e1cdfc92e", submodules=True
    )
    version(
        "2.1.0", tag="v2.1.0", commit="52e10c05cd40dfdfde186c1e63213695f5aeaf65", submodules=True
    )
    version(
        "2.0.0", tag="v2.0.0", commit="0dc8b4736357645b99632ee7c17a3dc6af771fbb", submodules=True
    )
    version(
        "1.1.0", tag="v1.1.0", commit="3db26e6a2626ee8c0cfa5c9769cfac6e33587122", submodules=True
    )
    version(
        "1.0.1", tag="v1.0.1", commit="a6741073431cab3a7a2434f9119a54d18e9978f4", submodules=True
    )
    version(
        "1.0.0", tag="v1.0.0", commit="82482fd7450ab378db110f06f7e0302112c22c05", submodules=True
    )
    version(
        "0.3.5", tag="v0.3.5", commit="a283977bb548cbaa0221bdb6c9832f7834f69e74", submodules=True
    )
    version(
        "0.3.4", tag="v0.3.4", commit="20a77408d8ae467af21d5802d14afe54f1253694", submodules=True
    )
    version(
        "0.3.3", tag="v0.3.3", commit="715a8bd003eb1d9db1e2ac7ff2c6251cfd445c27", submodules=True
    )
    version(
        "0.3.2", tag="v0.3.2", commit="06f37f2011fa4d9482f15e04fc206e2e7b7aa9e2", submodules=True
    )
    version(
        "0.3.1", tag="v0.3.1", commit="aef223065fdfe85d1e46bab95e3874821702891a", submodules=True
    )
    version(
        "0.3.0", tag="v0.3.0", commit="529004f9e88fbb49ee93a97465ff904be249039c", submodules=True
    )
    version(
        "0.2.4", tag="v0.2.4", commit="f774afae69b6f2e5c99ea8bf5660ccf68bd5436d", submodules=True
    )
    version(
        "0.2.3", tag="v0.2.3", commit="af158291f574701aabb6a2b16e6536aefaf4496e", submodules=True
    )
    version(
        "0.2.2", tag="v0.2.2", commit="68f4b86fd877c9ca00c9438c603e5dbc40d5f219", submodules=True
    )
    version(
        "0.2.1", tag="v0.2.1", commit="c22df368e2f52398351f49fbe2522bd1150ad171", submodules=True
    )
    version(
        "0.2.0", tag="v0.2.0", commit="7910b8d4dbfe83faacf65e864304ca916e34b86c", submodules=True
    )
    version(
        "0.1.4", tag="v0.1.4", commit="c2848289ba9d8c85346610d25af9531b82c50fc3", submodules=True
    )
    version(
        "0.1.3", tag="v0.1.3", commit="cc347edeb17f5f30f694aa47f395d17369a2e449", submodules=True
    )

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

    # https://github.com/LLNL/Umpire/pull/805
    patch(
        "https://github.com/LLNL/Umpire/pull/805/commits/47ff0aa1f7a01a917c3b7ac618e8a9e44a10fd25.patch?full_index=1",
        sha256="7ed5d2c315a3b31e339f664f6108e32d7cb4cb8e9f22e5c78a65ba02625ccc09",
        when="@2022.10.0",
    )

    # https://github.com/LLNL/Umpire/pull/816
    patch(
        "https://github.com/LLNL/Umpire/pull/816/commits/2292d1d6078f6d9523b7ad0886ffa053644569d5.patch?full_index=1",
        sha256="0f43cad7cdaec3c225ab6414ab9f81bd405a1157abf5a508e515bcb6ca53326d",
        when="@2022.10.0",
    )

    variant("fortran", default=False, description="Build C/Fortran API")
    variant("c", default=True, description="Build C API")
    variant("numa", default=False, description="Enable NUMA support")
    variant("shared", default=True, description="Enable Shared libs")
    variant("openmp", default=False, description="Build with OpenMP support")
    variant("deviceconst", default=False, description="Enables support for constant device memory")
    variant("examples", default=True, description="Build Umpire Examples")
    variant(
        "tests",
        default="none",
        values=("none", "basic", "benchmarks"),
        multi=False,
        description="Tests to run",
    )
    variant("device_alloc", default=True, description="Build Umpire Device Allocator")

    depends_on("cmake@3.8:", type="build")
    depends_on("cmake@3.9:", when="+cuda", type="build")
    depends_on("cmake@3.14:", when="@2022.03.0:", type="build")

    depends_on("blt@0.5.2:", type="build", when="@2022.10.0:")
    depends_on("blt@0.5.0:", type="build", when="@2022.03.0:")
    depends_on("blt@0.4.1", type="build", when="@6.0.0")
    depends_on("blt@0.4.0:", type="build", when="@4.1.3:5.0.1")
    depends_on("blt@0.3.6:", type="build", when="@:4.1.2")
    conflicts("^blt@:0.3.6", when="+rocm")

    depends_on("camp", when="@5.0.0:")
    depends_on("camp@0.2.2:0.2.3", when="@6.0.0")
    depends_on("camp@0.1.0", when="@5.0.0:5.0.1")
    depends_on("camp@2022.03.2:", when="@2022.03.0:")
    depends_on("camp@main", when="@main")
    depends_on("camp@main", when="@develop")
    depends_on("camp+openmp", when="+openmp")
    depends_on("camp~cuda", when="~cuda")

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
    conflicts("+device_alloc", when="@:2022.03.0")

    # device allocator exports device code, which requires static libs
    # currently only available for cuda.
    conflicts("+shared", when="+cuda")

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
        return "{0}-{1}-{2}@{3}.cmake".format(
            hostname,
            self._get_sys_type(self.spec),
            self.spec.compiler.name,
            self.spec.compiler.version,
        )

    def initconfig_compiler_entries(self):
        spec = self.spec
        entries = super().initconfig_compiler_entries()

        if "+rocm" in spec:
            entries.insert(0, cmake_cache_path("CMAKE_CXX_COMPILER", spec["hip"].hipcc))

        option_prefix = "UMPIRE_" if spec.satisfies("@2022.03.0:") else ""

        if "+fortran" in spec and self.compiler.fc is not None:
            entries.append(cmake_cache_option("ENABLE_FORTRAN", True))
        else:
            entries.append(cmake_cache_option("ENABLE_FORTRAN", False))

        entries.append(cmake_cache_option("{}ENABLE_C".format(option_prefix), "+c" in spec))

        return entries

    def initconfig_hardware_entries(self):
        spec = self.spec
        entries = super().initconfig_hardware_entries()

        option_prefix = "UMPIRE_" if spec.satisfies("@2022.03.0:") else ""

        if "+cuda" in spec:
            entries.append(cmake_cache_option("ENABLE_CUDA", True))

            if not spec.satisfies("cuda_arch=none"):
                cuda_arch = spec.variants["cuda_arch"].value
                entries.append(cmake_cache_string("CUDA_ARCH", "sm_{0}".format(cuda_arch[0])))
                entries.append(
                    cmake_cache_string("CMAKE_CUDA_ARCHITECTURES", "{0}".format(cuda_arch[0]))
                )
                flag = "-arch sm_{0}".format(cuda_arch[0])
                entries.append(cmake_cache_string("CMAKE_CUDA_FLAGS", "{0}".format(flag)))

            entries.append(
                cmake_cache_option(
                    "{}ENABLE_DEVICE_CONST".format(option_prefix), spec.satisfies("+deviceconst")
                )
            )
        else:
            entries.append(cmake_cache_option("ENABLE_CUDA", False))

        if "+rocm" in spec:
            entries.append(cmake_cache_option("ENABLE_HIP", True))
            entries.append(cmake_cache_path("HIP_ROOT_DIR", "{0}".format(spec["hip"].prefix)))
            hip_repair_cache(entries, spec)
            archs = self.spec.variants["amdgpu_target"].value
            if archs != "none":
                arch_str = ",".join(archs)
                entries.append(
                    cmake_cache_string("HIP_HIPCC_FLAGS", "--amdgpu-target={0}".format(arch_str))
                )
                entries.append(
                    cmake_cache_string("CMAKE_HIP_ARCHITECTURES", "{0}".format(arch_str))
                )
        else:
            entries.append(cmake_cache_option("ENABLE_HIP", False))

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
        entries.append(cmake_cache_option("{}ENABLE_NUMA".format(option_prefix), "+numa" in spec))
        entries.append(
            cmake_cache_option("{}ENABLE_OPENMP".format(option_prefix), "+openmp" in spec)
        )
        entries.append(cmake_cache_option("ENABLE_BENCHMARKS", "tests=benchmarks" in spec))
        entries.append(
            cmake_cache_option("{}ENABLE_EXAMPLES".format(option_prefix), "+examples" in spec)
        )
        entries.append(cmake_cache_option("{}ENABLE_DOCS".format(option_prefix), False))
        entries.append(
            cmake_cache_option("UMPIRE_ENABLE_DEVICE_ALLOCATOR", "+device_alloc" in spec)
        )
        entries.append(cmake_cache_option("BUILD_SHARED_LIBS", "+shared" in spec))
        entries.append(cmake_cache_option("ENABLE_TESTS", "tests=none" not in spec))

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
