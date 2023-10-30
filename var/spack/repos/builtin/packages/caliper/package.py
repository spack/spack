# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class Caliper(CachedCMakePackage, CudaPackage, ROCmPackage):
    """Caliper is a program instrumentation and performance measurement
    framework. It is designed as a performance analysis toolbox in a
    library, allowing one to bake performance analysis capabilities
    directly into applications and activate them at runtime.
    """

    homepage = "https://github.com/LLNL/Caliper"
    git = "https://github.com/LLNL/Caliper.git"
    url = "https://github.com/LLNL/Caliper/archive/v2.10.0.tar.gz"
    tags = ["e4s", "radiuss"]

    maintainers("daboehme")

    test_requires_compiler = True

    version("master", branch="master")
    version("2.10.0", sha256="14c4fb5edd5e67808d581523b4f8f05ace8549698c0e90d84b53171a77f58565")
    version("2.9.1", sha256="4771d630de505eff9227e0ec498d0da33ae6f9c34df23cb201b56181b8759e9e")
    version("2.9.0", sha256="507ea74be64a2dfd111b292c24c4f55f459257528ba51a5242313fa50978371f")
    version("2.8.0", sha256="17807b364b5ac4b05997ead41bd173e773f9a26ff573ff2fe61e0e70eab496e4")
    version(
        "2.7.0",
        sha256="b3bf290ec2692284c6b4f54cc0c507b5700c536571d3e1a66e56626618024b2b",
        deprecated=True,
    )
    version(
        "2.6.0",
        sha256="6efcd3e4845cc9a6169e0d934840766b12182c6d09aa3ceca4ae776e23b6360f",
        deprecated=True,
    )
    version(
        "2.5.0",
        sha256="d553e60697d61c53de369b9ca464eb30710bda90fba9671201543b64eeac943c",
        deprecated=True,
    )
    version(
        "2.4.0", tag="v2.4.0", commit="30577b4b8beae104b2b35ed487fec52590a99b3d", deprecated=True
    )
    version(
        "2.3.0", tag="v2.3.0", commit="9fd89bb0120750d1f9dfe37bd963e24e478a2a20", deprecated=True
    )
    version(
        "2.2.0", tag="v2.2.0", commit="c408e9b3642c7aa80eff37b0826d819c57e7bc04", deprecated=True
    )
    version(
        "2.1.1", tag="v2.1.1", commit="0593b0e01c1d8d3e50c990399cc0fee403485599", deprecated=True
    )
    version(
        "2.0.1", tag="v2.0.1", commit="4d7ff46381c53a461e62edd949e2d9dea9db7b08", deprecated=True
    )
    version(
        "1.9.1", tag="v1.9.1", commit="cfc1defbbee20b50dd3e3477badd09a92b1df970", deprecated=True
    )
    version(
        "1.9.0", tag="v1.9.0", commit="8356e747349b285aa621c5b74e71559f0babc4a1", deprecated=True
    )
    version(
        "1.8.0", tag="v1.8.0", commit="117c1ef596b617dc71407b8b67eebef094a654f8", deprecated=True
    )
    version(
        "1.7.0", tag="v1.7.0", commit="898277c93d884d4e7ca1ffcf3bbea81d22364f26", deprecated=True
    )

    is_linux = sys.platform.startswith("linux")
    variant("shared", default=True, description="Build shared libraries")
    variant("adiak", default=True, description="Enable Adiak support")
    variant("mpi", default=True, description="Enable MPI support")
    # libunwind has some issues on Mac
    variant(
        "libunwind", default=sys.platform != "darwin", description="Enable stack unwind support"
    )
    variant("libdw", default=is_linux, description="Enable DWARF symbol lookup")
    # pthread_self() signature is incompatible with PAPI_thread_init() on Mac
    variant("papi", default=sys.platform != "darwin", description="Enable PAPI service")
    variant("libpfm", default=False, description="Enable libpfm (perf_events) service")
    # Gotcha is Linux-only
    variant("gotcha", default=is_linux, description="Enable GOTCHA support")
    variant("sampler", default=is_linux, description="Enable sampling support on Linux")
    variant("sosflow", default=False, description="Enable SOSflow support")
    variant("fortran", default=False, description="Enable Fortran support")
    variant("variorum", default=False, description="Enable Variorum support")
    variant("kokkos", default=True, when="@2.3.0:", description="Enable Kokkos profiling support")
    variant("tests", default=False, description="Enable tests")

    depends_on("adiak@0.1:0", when="@2.2: +adiak")

    depends_on("papi@5.3:5", when="@:2.2 +papi")
    depends_on("papi@5.3:6", when="@2.3: +papi")

    depends_on("libpfm4@4.8:4", when="+libpfm")

    depends_on("mpi", when="+mpi")
    depends_on("unwind@1.2:1", when="+libunwind")
    depends_on("elfutils", when="+libdw")
    depends_on("variorum", when="+variorum")

    depends_on("sosflow@spack", when="@1.0:1+sosflow")

    depends_on("cmake", type="build")
    depends_on("python", type="build")

    # sosflow support not yet in 2.0
    conflicts("+sosflow", "@2.0.0:2.9")
    conflicts("+adiak", "@:2.1")
    conflicts("+libdw", "@:2.4")
    conflicts("+rocm", "@:2.7")
    conflicts("+rocm+cuda")

    patch("for_aarch64.patch", when="target=aarch64:")
    patch(
        "sampler-service-missing-libunwind-include-dir.patch",
        when="@2.9.0:2.9.1 +libunwind +sampler",
    )

    def _get_sys_type(self, spec):
        sys_type = spec.architecture
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        return sys_type

    def initconfig_compiler_entries(self):
        spec = self.spec
        entries = super(Caliper, self).initconfig_compiler_entries()

        if "+fortran" in spec:
            entries.append(cmake_cache_option("WITH_FORTRAN", True))

        entries.append(cmake_cache_option("BUILD_SHARED_LIBS", "+shared" in spec))
        entries.append(cmake_cache_option("BUILD_TESTING", "+tests" in spec))
        entries.append(cmake_cache_option("BUILD_DOCS", False))
        entries.append(cmake_cache_path("PYTHON_EXECUTABLE", spec["python"].command.path))

        return entries

    def initconfig_hardware_entries(self):
        spec = self.spec
        entries = super(Caliper, self).initconfig_hardware_entries()

        entries.append("#------------------{0}".format("-" * 30))
        entries.append("# Package custom hardware settings")
        entries.append("#------------------{0}\n".format("-" * 30))
        if "+cuda" in spec:
            entries.append(cmake_cache_option("WITH_CUPTI", True))
            entries.append(cmake_cache_option("WITH_NVTX", True))
            entries.append(cmake_cache_path("CUPTI_PREFIX", spec["cuda"].prefix))
        if "+rocm" in spec:
            entries.append(cmake_cache_option("WITH_ROCTRACER", True))
            entries.append(cmake_cache_option("WITH_ROCTX", True))
            # entries.append(cmake_cache_option("ROCM_ROOT_DIR", "/usr/"))

        return entries

    def initconfig_mpi_entries(self):
        spec = self.spec
        entries = super(Caliper, self).initconfig_mpi_entries()

        entries.append(cmake_cache_option("WITH_MPI", "+mpi" in spec))

        return entries

    def initconfig_package_entries(self):
        spec = self.spec
        entries = []

        if "+adiak" in spec:
            entries.append(cmake_cache_option("WITH_ADIAK", True))
        if "+gotcha" in spec:
            entries.append(cmake_cache_option("WITH_GOTCHA", True))
        if "+sampler" in spec:
            entries.append(cmake_cache_option("WITH_SAMPLER", True))
        if "+papi" in spec:
            entries.append(cmake_cache_option("WITH_PAPI", True))
            # use pre installed papi
            entries.append(cmake_cache_path("PAPI_PREFIX", spec["papi"].prefix))
        if "+libdw" in spec:
            entries.append(cmake_cache_option("WITH_LIBDW", True))
            entries.append(cmake_cache_path("LIBDW_PREFIX", spec["elfutils"].prefix))
        if "+libpfm" in spec:
            entries.append(cmake_cache_option("WITH_LIBPFM", True))
            entries.append(cmake_cache_path("LIBPFM_INSTALL", spec["libpfm4"].prefix))
        if "+sosflow" in spec:
            entries.append(cmake_cache_option("WITH_SOSFLOW", True))
            entries.append(cmake_cache_path("SOS_PREFIX", spec["sosflow"].prefix))
        if "+kokkos" in spec:
            entries.append(cmake_cache_option("WITH_KOKKOS", True))
        if "+variorum" in spec:
            entries.append(cmake_cache_option("WITH_VARIORUM", True))
            entries.append(cmake_cache_path("VARIORUM_PREFIX", spec["variorum"].prefix))
        # -DWITH_CALLPATH was renamed -DWITH_LIBUNWIND in 2.5
        callpath_flag = "LIBUNWIND" if spec.satisfies("@2.5:") else "CALLPATH"
        if "+libunwind" in spec:
            entries.append(cmake_cache_path("LIBUNWIND_PREFIX", spec["unwind"].prefix))
            entries.append(cmake_cache_option("WITH_%s" % callpath_flag, True))
        else:
            entries.append(cmake_cache_option("WITH_%s" % callpath_flag, False))

        return entries

    def cmake_args(self):
        return []

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources([join_path("examples", "apps")])

    def test_cxx_example(self):
        """build and run cxx-example"""

        exe = "cxx-example"
        source_file = "{0}.cpp".format(exe)

        source_path = find_required_file(
            self.test_suite.current_test_cache_dir, source_file, expected=1, recursive=True
        )

        lib_dir = self.prefix.lib if os.path.exists(self.prefix.lib) else self.prefix.lib64

        cxx = which(os.environ["CXX"])
        test_dir = os.path.dirname(source_path)
        with working_dir(test_dir):
            cxx(
                "-L{0}".format(lib_dir),
                "-I{0}".format(self.prefix.include),
                source_path,
                "-o",
                exe,
                "-std=c++11",
                "-lcaliper",
                "-lstdc++",
            )

            cxx_example = which(exe)
            cxx_example()
