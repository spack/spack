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
    url = "https://github.com/LLNL/RAJA/releases/download/v2022.03.0/RAJA-v2022.03.0.tar.gz"
    git = "https://github.com/LLNL/RAJA.git"
    tags = ["radiuss", "e4s"]

    maintainers("davidbeckingsale")

    version("develop", branch="develop", submodules=False)
    version("main", branch="main", submodules=False)
    version("2023.06.1", sha256="1a26b186624d9c8ebab728842f567a75868cd9cbf364e782fe0720e54b2d30b0")
    version("2023.06.0", sha256="934dc1e7a3e64fe1716a730c67483f224b1ed3a7fccdae25f87bd0984a2e7f41")
    version("2022.10.5", sha256="2d4bcb90cd8997c3a2e91dd3b453ee6bb61f4eaebd125a719c34d0235d0a44a0")
    version("2022.10.4", sha256="359eec3955722d6853d92ede98156b01e2191bf313ef1dd47940a8812355d509")
    version("2022.10.3", sha256="63e4fd11cd84639db052dc3410cabd720d83bde68a2fe5a4e75e6577dd830819")
    version("2022.10.2", sha256="60d119701b44b89dfaf0d28295347f68be92803d9481e3d1cb619bf20c03c029")
    version("2022.10.1", sha256="08c50406ccc7b2290bb8632503f4c1234179df41e6060ff07794a9ceedbc1f15")
    version("2022.10.0", sha256="05b4c7bc258a975fc6b0e1bb440f5f9e37ddcdd53b8fc1d3ae58a29881a9539e")
    version("2022.03.1", sha256="fbdf291ee205fe01f01bedf29d2b6334235fa49992c60658736c66dc212c706c")
    version("2022.03.0", sha256="7d3be428947e1c191f6fab0e2f276e2fa087207bc2ebd13bd17c7c9a54efccac")
    version("0.14.1", sha256="343c091502dafd41f94a3d868821dc9f5c24aa2224147ea0b49c331172d72b82")
    version("0.14.0", sha256="0966472b5b7eb6582296d24d910d4288ac0834d51796455a6bd2b7da3bc024d2")
    version("0.13.0", sha256="f34f783797b589c438436cba847d94d4c8ee1cebc309417759fae99ccd6a5152")
    version("0.12.1", sha256="e6cf53756d2273b21cdf7fb624703bf326633fad9fee3873c58fae6cf3156176")
    version("0.12.0", sha256="4b58a67fca9020330dda9d1d08c03a650d67391f23abe69d48a07482d83e6d8f")
    version("0.11.0", sha256="447726dc8f4c51d5a769f080b13652064bcc9eddb10b2d6014174f796aa28f39")
    version("0.10.1", sha256="d4e0153c6f118618731ea310351f3cce2566e9d92616afe2478c3d7c090915b1")
    version("0.10.0", sha256="654ab55f0dad594da597499a6c109b5a1995c91e844b6162f82376f2d4f1b730")
    version("0.9.0", sha256="b251f06676d88e2fa3ef30ccac04d55655318429a9ef1e008888b901593c5b3a")
    version("0.8.0", sha256="c397b998bb3c847c6af03e44d85a2151b76a100bb2e883f28453f3689d90d394")
    version("0.7.0", sha256="4127598d226936c0ea8d6e0b40da1049e65fce8efd0359bd391ec4ad7e4ecdcd")
    version("0.6.0", sha256="d4435b5ff48443ea253d41df02b6d2988645eb79590cb3be1601664d4356e654")
    version("0.5.3", sha256="f27d05ac77c13f4304967991539c34f946b05ee2d4628c2dcd9637c94b25e56f")
    version("0.5.2", sha256="49d8ac6061ef3cda35c00c1d76ce5f52e4de49984863fcb28217331cf5f6a190")
    version("0.5.1", sha256="af322bc890ed763db815d19ebe1fdb3c4c2b33855b10cdeb99b95a835f93b86e")
    version("0.5.0", sha256="fde0a29a4f4cb35a66d9c0b34170b5bde2ceff8f8291d0c9166e9e0761012f22")
    version("0.4.1", sha256="921d286b307215e2fa61c8424ba8039b145d3c4545bc7f12d9787e82e3bc8957")
    version("0.4.0", sha256="ec90f91568dc9125b9150463259d069ea7ba52b38814aeb024e37708f27d2c43")

    # export targets when building pre-2.4.0 release with BLT 0.4.0+
    patch(
        "https://github.com/LLNL/RAJA/commit/eca1124ee4af380d6613adc6012c307d1fd4176b.patch?full_index=1",
        sha256="12bb78c00b6683ad3e7fd4e3f87f9776bae074b722431b79696bc862816735ef",
        when="@:0.13.0 ^blt@0.4:",
    )

    variant("openmp", default=True, description="Build OpenMP backend")
    variant("shared", default=True, description="Build Shared Libs")
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
    depends_on("cmake@3.14:", when="@2022.03.0:")

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
