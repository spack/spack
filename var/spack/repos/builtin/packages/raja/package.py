# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import socket

from spack.package import *
from spack.pkg.builtin.camp import hip_repair_cache


class Raja(CachedCMakePackage, CudaPackage, ROCmPackage):
    """RAJA Parallel Framework."""

    homepage = "https://software.llnl.gov/RAJA/"
    git = "https://github.com/LLNL/RAJA.git"
    tags = ["radiuss", "e4s"]

    maintainers("davidbeckingsale")

    version("develop", branch="develop", submodules=False)
    version("main", branch="main", submodules=False)
    version(
        "2022.10.4",
        tag="v2022.10.4",
        commit="c2a6b1740759ae3ae7c85b35e20dbffbe235355d",
        submodules=False,
    )
    version(
        "2022.03.0",
        tag="v2022.03.0",
        commit="4351fe6a50bd579511a625b017c9e054885e7fd2",
        submodules=False,
    )
    version(
        "0.14.0",
        tag="v0.14.0",
        commit="357933a42842dd91de5c1034204d937fce0a2a44",
        submodules="True",
    )
    version(
        "0.13.0",
        tag="v0.13.0",
        commit="3047fa720132d19ee143b1fcdacaa72971f5988c",
        submodules="True",
    )
    version(
        "0.12.1",
        tag="v0.12.1",
        commit="9cb6370bb2868e35ebba23cdce927f5f7f9da530",
        submodules="True",
    )
    version(
        "0.12.0",
        tag="v0.12.0",
        commit="32d92e38da41cc8d4db25ec79b9884a73a0cb3a1",
        submodules="True",
    )
    version(
        "0.11.0",
        tag="v0.11.0",
        commit="0502b9b69c4cb60aa0afbdf699b555c76cb18f22",
        submodules="True",
    )
    version(
        "0.10.1",
        tag="v0.10.1",
        commit="be91e040130678b1350dbda56cc352433db758bd",
        submodules="True",
    )
    version(
        "0.10.0",
        tag="v0.10.0",
        commit="53cb89cf788d28bc4ed2b4e6f75483fdd26024aa",
        submodules="True",
    )
    version(
        "0.9.0", tag="v0.9.0", commit="df7ca1fa892b6ac4147c614d2d739d5022f63fc7", submodules="True"
    )
    version(
        "0.8.0", tag="v0.8.0", commit="8d19a8c2cbac611de6f92ad8852b9f3454b27e63", submodules="True"
    )
    version(
        "0.7.0", tag="v0.7.0", commit="caa33b371b586dfae3d8569caee91c5eddfd7b31", submodules="True"
    )
    version(
        "0.6.0", tag="v0.6.0", commit="cc7a97e8b4e52c3de820c9dfacd358822a147871", submodules="True"
    )
    version(
        "0.5.3", tag="v0.5.3", commit="1ca35c0ed2a43a3fa9c6cd70c5d25f16d88ecd8c", submodules="True"
    )
    version(
        "0.5.2", tag="v0.5.2", commit="4d5c3d5d7f311838855f7010810610349e729f64", submodules="True"
    )
    version(
        "0.5.1", tag="v0.5.1", commit="bf340abe5199d7e051520913c9a7a5de336b5820", submodules="True"
    )
    version(
        "0.5.0", tag="v0.5.0", commit="9b539d84fdad049f65caeba836f41031f5baf4cc", submodules="True"
    )
    version(
        "0.4.1", tag="v0.4.1", commit="3618cfe95d6a442fa50fbe7bfbcf654cf9f800b9", submodules="True"
    )
    version(
        "0.4.0", tag="v0.4.0", commit="31b2a48192542c2da426885baa5af0ed57606b78", submodules="True"
    )

    # export targets when building pre-2.4.0 release with BLT 0.4.0+
    patch(
        "https://github.com/LLNL/RAJA/commit/eca1124ee4af380d6613adc6012c307d1fd4176b.patch?full_index=1",
        sha256="12bb78c00b6683ad3e7fd4e3f87f9776bae074b722431b79696bc862816735ef",
        when="@:0.13.0 ^blt@0.4:",
    )

    variant("openmp", default=True, description="Build OpenMP backend")
    variant("shared", default=True, description="Build Shared Libs")
    variant("plugins", default=False, description="Enable runtime plugins")
    variant("examples", default=True, description="Build examples.")
    variant("exercises", default=True, description="Build exercises.")
    # TODO: figure out gtest dependency and then set this default True
    # and remove the +tests conflict below.
    variant("tests", default=False, description="Build tests")

    depends_on("blt", type="build")
    depends_on("blt@0.5.0:", type="build", when="@0.14.1:")
    depends_on("blt@0.4.1", type="build", when="@0.14.0")
    depends_on("blt@0.4.0:", type="build", when="@0.13.0")
    depends_on("blt@0.3.6:", type="build", when="@:0.12.0")
    conflicts("^blt@:0.3.6", when="+rocm")

    depends_on("camp@0.2.2:0.2.3", when="@0.14.0")
    depends_on("camp@0.1.0", when="@0.10.0:0.13.0")
    depends_on("camp@2022.03.2:2022.03", when="@2022.03.0:2022.03")
    depends_on("camp@2022.10:", when="@2022.10:")
    depends_on("camp@main", when="@main")
    depends_on("camp@main", when="@develop")
    depends_on("camp+openmp", when="+openmp")

    depends_on("cmake@:3.20", when="@:2022.03+rocm", type="build")
    depends_on("cmake@3.23:", when="@2022.10:+rocm", type="build")
    depends_on("cmake@3.14:", when="@2022.03.0:", type="build")

    depends_on("llvm-openmp", when="+openmp %apple-clang")

    depends_on("rocprim", when="+rocm")
    with when("+rocm @0.12.0:"):
        depends_on("camp+rocm")
        for arch in ROCmPackage.amdgpu_targets:
            depends_on(
                "camp+rocm amdgpu_target={0}".format(arch), when="amdgpu_target={0}".format(arch)
            )
        conflicts("+openmp")

    with when("+cuda @0.12.0:"):
        depends_on("camp+cuda")
        for sm_ in CudaPackage.cuda_arch_values:
            depends_on("camp +cuda cuda_arch={0}".format(sm_), when="cuda_arch={0}".format(sm_))

    def _get_sys_type(self, spec):
        sys_type = spec.architecture
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        return sys_type

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libRAJA", root=self.prefix, shared=shared, recursive=True)

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
        return entries

    def initconfig_hardware_entries(self):
        spec = self.spec
        entries = super().initconfig_hardware_entries()

        entries.append(cmake_cache_option("ENABLE_OPENMP", "+openmp" in spec))

        if "+cuda" in spec:
            entries.append(cmake_cache_option("ENABLE_CUDA", True))

            if not spec.satisfies("cuda_arch=none"):
                cuda_arch = spec.variants["cuda_arch"].value
                entries.append(cmake_cache_string("CUDA_ARCH", "sm_{0}".format(cuda_arch[0])))
                entries.append(
                    cmake_cache_string("CMAKE_CUDA_ARCHITECTURES", "{0}".format(cuda_arch[0]))
                )
        else:
            entries.append(cmake_cache_option("ENABLE_CUDA", False))

        if "+rocm" in spec:
            entries.append(cmake_cache_option("ENABLE_HIP", True))
            entries.append(cmake_cache_path("HIP_ROOT_DIR", "{0}".format(spec["hip"].prefix)))
            hip_repair_cache(entries, spec)
            hipcc_flags = []
            if self.spec.satisfies("@0.14.0"):
                hipcc_flags.append("-std=c++14")
            archs = self.spec.variants["amdgpu_target"].value
            if archs != "none":
                arch_str = ",".join(archs)
                hipcc_flags.append("--amdgpu-target={0}".format(arch_str))
            entries.append(cmake_cache_string("HIP_HIPCC_FLAGS", " ".join(hipcc_flags)))
        else:
            entries.append(cmake_cache_option("ENABLE_HIP", False))

        return entries

    def initconfig_package_entries(self):
        spec = self.spec
        entries = []

        option_prefix = "RAJA_" if spec.satisfies("@0.14.0:") else ""

        entries.append(cmake_cache_path("BLT_SOURCE_DIR", spec["blt"].prefix))
        if "camp" in self.spec:
            entries.append(cmake_cache_path("camp_DIR", spec["camp"].prefix))
        entries.append(cmake_cache_option("BUILD_SHARED_LIBS", "+shared" in spec))
        entries.append(cmake_cache_option("RAJA_ENABLE_RUNTIME_PLUGINS", "+plugins" in spec))
        entries.append(
            cmake_cache_option("{}ENABLE_EXAMPLES".format(option_prefix), "+examples" in spec)
        )
        if spec.satisfies("@0.14.0:"):
            entries.append(
                cmake_cache_option(
                    "{}ENABLE_EXERCISES".format(option_prefix), "+exercises" in spec
                )
            )
        else:
            entries.append(cmake_cache_option("ENABLE_EXERCISES", "+exercises" in spec))

        # Work around spack adding -march=ppc64le to SPACK_TARGET_ARGS which
        # is used by the spack compiler wrapper.  This can go away when BLT
        # removes -Werror from GTest flags
        if self.spec.satisfies("%clang target=ppc64le:") or not self.run_tests:
            entries.append(cmake_cache_option("ENABLE_TESTS", False))
        else:
            entries.append(cmake_cache_option("ENABLE_TESTS", True))

        return entries

    def cmake_args(self):
        options = []
        return options

    @property
    def build_relpath(self):
        """Relative path to the cmake build subdirectory."""
        return join_path("..", self.build_dirname)

    @run_after("install")
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to a
        relative install test subdirectory for use during `spack test run`."""
        # Now copy the relative files
        self.cache_extra_test_sources(self.build_relpath)

        # Ensure the path exists since relying on a relative path at the
        # same level as the normal stage source path.
        mkdirp(self.install_test_root)

    @property
    def _extra_tests_path(self):
        # TODO: The tests should be converted to re-build and run examples
        # TODO: using the installed libraries.
        return join_path(self.install_test_root, self.build_relpath, "bin")

    def _test_examples(self):
        """Perform very basic checks on a subset of copied examples."""
        checks = [
            (
                "ex5_line-of-sight_solution",
                [r"RAJA sequential", r"RAJA OpenMP", r"result -- PASS"],
            ),
            (
                "ex6_stencil-offset-layout_solution",
                [r"RAJA Views \(permuted\)", r"result -- PASS"],
            ),
            (
                "ex8_tiled-matrix-transpose_solution",
                [r"parallel top inner loop", r"collapsed inner loops", r"result -- PASS"],
            ),
            ("kernel-dynamic-tile", [r"Running index", r"(24,24)"]),
            ("plugin-example", [r"Launching host kernel for the 10 time"]),
            ("tut_batched-matrix-multiply", [r"result -- PASS"]),
            ("wave-eqn", [r"Max Error = 2", r"Evolved solution to time"]),
        ]
        for exe, expected in checks:
            reason = "test: checking output of {0} for {1}".format(exe, expected)
            self.run_test(
                exe,
                [],
                expected,
                installed=False,
                purpose=reason,
                skip_missing=True,
                work_dir=self._extra_tests_path,
            )

    def test(self):
        """Perform smoke tests."""
        self._test_examples()
