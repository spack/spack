# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class Ginkgo(CMakePackage, CudaPackage, ROCmPackage):
    """High-performance linear algebra library for manycore systems,
    with a focus on sparse solution of linear systems."""

    homepage = "https://ginkgo-project.github.io/"
    git = "https://github.com/ginkgo-project/ginkgo.git"

    maintainers("tcojean", "hartwiganzt")

    tags = ["e4s"]

    version("develop", branch="develop")
    version("master", branch="master")
    version("1.5.0", commit="234594c92b58e2384dfb43c2d08e7f43e2b58e7a", preferred=True)  # v1.5.0
    version("1.5.0.glu_experimental", branch="glu_experimental")
    version("1.4.0", commit="f811917c1def4d0fcd8db3fe5c948ce13409e28e")  # v1.4.0
    version("1.3.0", commit="4678668c66f634169def81620a85c9a20b7cec78")  # v1.3.0
    version("1.2.0", commit="b4be2be961fd5db45c3d02b5e004d73550722e31")  # v1.2.0
    version("1.1.1", commit="08d2c5200d3c78015ac8a4fd488bafe1e4240cf5")  # v1.1.1
    version("1.1.0", commit="b9bec8225442b3eb2a85a870efa112ab767a17fb")  # v1.1.0
    version("1.0.0", commit="45244641e0c2b19ba33aecd25153c0bddbcbe1a0")  # v1.0.0

    variant("shared", default=True, description="Build shared libraries")
    variant("full_optimizations", default=False, description="Compile with all optimizations")
    variant("openmp", default=sys.platform != "darwin", description="Build with OpenMP")
    variant("oneapi", default=False, description="Build with oneAPI support")
    variant("develtools", default=False, description="Compile with develtools enabled")
    variant("hwloc", default=False, description="Enable HWLOC support")
    variant("mpi", default=False, description="Enable MPI support")
    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )

    depends_on("cmake@3.9:", type="build")
    depends_on("cuda@9:", when="+cuda")
    depends_on("mpi", when="+mpi")

    depends_on("rocthrust", when="+rocm")
    depends_on("hipsparse", when="+rocm")
    depends_on("hipblas", when="+rocm")
    depends_on("rocrand", when="+rocm")
    # ROCPRIM is not a direct dependency, but until we have reviewed our CMake
    # setup for rocthrust, this needs to also be added here.
    depends_on("rocprim", when="+rocm")
    depends_on("hwloc@2.1:", when="+hwloc")

    depends_on("googletest", type="test")
    depends_on("numactl", type="test", when="+hwloc")

    depends_on("intel-oneapi-mkl", when="+oneapi")
    depends_on("intel-oneapi-dpl", when="+oneapi")

    conflicts("%gcc@:5.2.9")
    conflicts("+rocm", when="@:1.1.1")
    conflicts("+mpi", when="@:1.4.0")
    conflicts("+cuda", when="+rocm")
    conflicts("+openmp", when="+oneapi")

    # ROCm 4.1.0 breaks platform settings which breaks Ginkgo's HIP support.
    conflicts("^hip@4.1.0:", when="@:1.3.0")
    conflicts("^hipblas@4.1.0:", when="@:1.3.0")
    conflicts("^hipsparse@4.1.0:", when="@:1.3.0")
    conflicts("^rocthrust@4.1.0:", when="@:1.3.0")
    conflicts("^rocprim@4.1.0:", when="@:1.3.0")

    # Skip smoke tests if compatible hardware isn't found
    patch("1.4.0_skip_invalid_smoke_tests.patch", when="@master")
    patch("1.4.0_skip_invalid_smoke_tests.patch", when="@1.4.0")

    # Newer DPC++ compilers use the updated SYCL 2020 standard which change
    # kernel attribute propagation rules. This doesn't work well with the
    # initial Ginkgo oneAPI support.
    patch("1.4.0_dpcpp_use_old_standard.patch", when="+oneapi @master")
    patch("1.4.0_dpcpp_use_old_standard.patch", when="+oneapi @1.4.0")

    # Add missing include statement
    patch("thrust-count-header.patch", when="+rocm @1.5.0:")

    def setup_build_environment(self, env):
        spec = self.spec
        if "+oneapi" in spec:
            env.set("MKLROOT", join_path(spec["intel-oneapi-mkl"].prefix, "mkl", "latest"))
            env.set("DPL_ROOT", join_path(spec["intel-oneapi-dpl"].prefix, "dpl", "latest"))

    def cmake_args(self):
        # Check that the have the correct C++ standard is available
        if self.spec.satisfies("@:1.2.0"):
            try:
                self.compiler.cxx11_flag
            except UnsupportedCompilerFlag:
                raise InstallError("Ginkgo requires a C++11-compliant C++ compiler")
        else:
            try:
                self.compiler.cxx14_flag
            except UnsupportedCompilerFlag:
                raise InstallError("Ginkgo requires a C++14-compliant C++ compiler")

        cxx_is_dpcpp = os.path.basename(self.compiler.cxx) == "dpcpp"
        if self.spec.satisfies("+oneapi") and not cxx_is_dpcpp:
            raise InstallError(
                "Ginkgo's oneAPI backend requires the" + "DPC++ compiler as main CXX compiler."
            )

        spec = self.spec
        from_variant = self.define_from_variant
        args = [
            from_variant("GINKGO_BUILD_CUDA", "cuda"),
            from_variant("GINKGO_BUILD_HIP", "rocm"),
            from_variant("GINKGO_BUILD_DPCPP", "oneapi"),
            from_variant("GINKGO_BUILD_OMP", "openmp"),
            from_variant("GINKGO_BUILD_MPI", "mpi"),
            from_variant("BUILD_SHARED_LIBS", "shared"),
            from_variant("GINKGO_JACOBI_FULL_OPTIMIZATIONS", "full_optimizations"),
            from_variant("GINKGO_BUILD_HWLOC", "hwloc"),
            from_variant("GINKGO_DEVEL_TOOLS", "develtools"),
            # As we are not exposing benchmarks, examples, tests nor doc
            # as part of the installation, disable building them altogether.
            "-DGINKGO_BUILD_BENCHMARKS=OFF",
            "-DGINKGO_BUILD_DOC=OFF",
            "-DGINKGO_BUILD_EXAMPLES=OFF",
            "-DGINKGO_WITH_CCACHE=OFF",
            self.define("GINKGO_BUILD_TESTS", self.run_tests),
            # Let spack handle the RPATH
            "-DGINKGO_INSTALL_RPATH=OFF",
        ]

        if self.run_tests:
            args.append("-DGINKGO_USE_EXTERNAL_GTEST=ON")

        if "+cuda" in spec:
            archs = spec.variants["cuda_arch"].value
            if archs != "none":
                arch_str = ";".join(archs)
                args.append("-DGINKGO_CUDA_ARCHITECTURES={0}".format(arch_str))

        if "+rocm" in spec:
            args.append("-DHIP_PATH={0}".format(spec["hip"].prefix))
            args.append("-DHIP_CLANG_PATH={0}/bin".format(spec["llvm-amdgpu"].prefix))
            args.append("-DHIP_CLANG_INCLUDE_PATH={0}/include".format(spec["llvm-amdgpu"].prefix))
            args.append("-DHIPSPARSE_PATH={0}".format(spec["hipsparse"].prefix))
            args.append("-DHIPBLAS_PATH={0}".format(spec["hipblas"].prefix))
            args.append("-DHIPRAND_PATH={0}/hiprand".format(spec["rocrand"].prefix))
            args.append("-DROCRAND_PATH={0}/rocrand".format(spec["rocrand"].prefix))
            args.append("-DROCPRIM_INCLUDE_DIRS={0}".format(spec["rocprim"].prefix.include))
            archs = self.spec.variants["amdgpu_target"].value
            if archs != "none":
                arch_str = ";".join(archs)
                args.append("-DGINKGO_HIP_AMDGPU={0}".format(arch_str))
            if spec.satisfies("^hip@5.2.0:"):
                args.append(
                    self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip)
                )
        return args

    extra_install_tests = join_path("test", "test_install")

    @run_after("install")
    def cache_test_sources(self):
        self.cache_extra_test_sources(self.extra_install_tests)

    @property
    def _cached_tests_src_dir(self):
        """The cached smoke test source directory."""
        return join_path(self.test_suite.current_test_cache_dir, self.extra_install_tests)

    @property
    def _cached_tests_work_dir(self):
        """The working directory for cached test sources."""
        return join_path(self._cached_tests_src_dir, "build")

    def _build_test(self):
        cmake_bin = join_path(self.spec["cmake"].prefix.bin, "cmake")
        cmake_args = [
            "-DCMAKE_C_COMPILER={0}".format(self.compiler.cc),
            "-DCMAKE_CXX_COMPILER={0}".format(self.compiler.cxx),
            self._cached_tests_src_dir,
        ]

        # Fix: For HIP tests, add the ARCH compilation flags when not present
        if "+rocm" in self.spec:
            src_path = join_path(self._cached_tests_src_dir, "CMakeLists.txt")
            cmakelists = open(src_path, "rt")
            data = cmakelists.read()
            data = data.replace(
                'CLANG_OPTIONS "${GINKGO_PIC_OPTION}"',
                'CLANG_OPTIONS "${GINKGO_AMD_ARCH_FLAGS}" "${GINKGO_PIC_OPTION}"',
            )
            cmakelists.close()
            cmakelists = open(src_path, "wt")
            cmakelists.write(data)
            cmakelists.close()

        if not self.run_test(
            cmake_bin,
            options=cmake_args,
            purpose="Generate the Makefile",
            work_dir=self._cached_tests_work_dir,
        ):
            print("Skipping Ginkgo test: failed to generate Makefile")
            return

        if not self.run_test(
            "make", purpose="Build test software", work_dir=self._cached_tests_work_dir
        ):
            print("Skipping Ginkgo test: failed to build test")
            return

    def test(self):
        """Run the smoke tests."""
        # For now only 1.4.0 and later releases support this scheme.
        if self.spec.satisfies("@:1.3.0"):
            print("SKIPPED: smoke tests not supported with this Ginkgo version.")
            return

        self._build_test()

        # Perform the test(s) created by setup_build_tests.
        files = [
            ("test_install", [r"REFERENCE", r"correctly detected and is complete"]),
            ("test_install_cuda", [r"CUDA", r"correctly detected and is complete"]),
            ("test_install_hip", [r"HIP", r"correctly detected and is complete"]),
        ]
        for f, expected in files:
            self.run_test(
                f,
                [],
                expected,
                skip_missing=True,
                installed=False,
                purpose="test: Running {0}".format(f),
                work_dir=self._cached_tests_work_dir,
            )
