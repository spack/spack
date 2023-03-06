# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# ----------------------------------------------------------------------------

from spack.package import *


class Omnitrace(CMakePackage):
    """Application Profiling, Tracing, and Analysis"""

    homepage = "https://amdresearch.github.io/omnitrace"
    git = "https://github.com/AMDResearch/omnitrace.git"
    maintainers("jrmadsen")

    version("main", branch="main", submodules=True)
    version("1.7.4", commit="12001d9633328f9f56210c7ebffce065bff06310", submodules=True)
    version("1.7.3", commit="2ebfe3fc30f977559142509edc4ea190c975992a", submodules=True)
    version("1.7.2", commit="a41a5c155e0d3780de4c83a76f28d7c8ffa6414f", submodules=True)
    version("1.7.1", commit="67f7471253b8e031e476d80d2bc00e569285c1bf", submodules=True)
    version("1.7.0", commit="2a387f909935d06c6a4874a5b11f38fb8521800e", submodules=True)
    version("1.6.0", commit="15e6e6d979fcd5f549d952862400f292ec735b8c", submodules=True)
    version("1.5.0", commit="2718596e5a6808a9278c3f6c8fddfaf977d3bcb6", submodules=True)
    version("1.4.0", commit="23fb3946c7f4c0702b1b168e1d78b8b62597e3f1", submodules=True)
    version("1.3.1", commit="641225f88304909fd2ca5407aec062d0fdf0ed8b", submodules=True)
    version("1.3.0", commit="4dd144a32c8b83c44e132ef53f2b44fe4b4d5569", submodules=True)
    version("1.2.0", commit="f82845388aab108ed1d1fc404f433a0def391bb3", submodules=True)

    # override build_type to default to Release because this has a significant
    # impact on build-time and the size of the build
    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
    )
    variant(
        "rocm",
        default=True,
        description="Enable ROCm API, kernel tracing, and GPU HW counters support",
    )
    variant("strip", default=False, description="Faster binary instrumentation, worse debugging")
    variant(
        "python", default=False, description="Enable support for Python function profiling and API"
    )
    variant("papi", default=True, description="Enable HW counters support via PAPI")
    variant("ompt", default=True, description="Enable OpenMP Tools support")
    variant(
        "tau",
        default=False,
        description="Enable support for using TAU markers in omnitrace instrumentation",
    )
    variant(
        "caliper",
        default=False,
        description="Enable support for using Caliper markers in omnitrace instrumentation",
    )
    variant(
        "perfetto_tools",
        default=False,
        description="Install perfetto tools (e.g. traced, perfetto)",
    )
    variant(
        "mpi",
        default=False,
        description=(
            "Enable intercepting MPI functions and aggregating output during finalization "
            "(requires target application to use same MPI installation)"
        ),
    )
    variant(
        "mpi_headers",
        default=True,
        description=(
            "Enable intercepting MPI functions but w/o support for aggregating output "
            "(target application can use any MPI installation)"
        ),
    )

    extends("python", when="+python")

    # hard dependencies
    depends_on("cmake@3.16:", type="build")
    depends_on("dyninst@11.0.1:", type=("build", "run"))
    depends_on("libunwind", type=("build", "run"))

    # soft dependencies
    depends_on("hip", when="+rocm")
    depends_on("rocm-smi-lib", when="+rocm")
    depends_on("roctracer-dev", when="+rocm")
    depends_on("rocprofiler-dev", when="@1.3.0: +rocm")
    depends_on("papi+shared", when="+papi")
    depends_on("mpi", when="+mpi")
    depends_on("tau", when="+tau")
    depends_on("caliper", when="+caliper")
    depends_on("python@3:", when="+python", type=("build", "run"))

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define("SPACK_BUILD", True),
            self.define("OMNITRACE_BUILD_PAPI", False),
            self.define("OMNITRACE_BUILD_PYTHON", True),
            self.define("OMNITRACE_BUILD_DYNINST", False),
            self.define("OMNITRACE_BUILD_LIBUNWIND", False),
            self.define("OMNITRACE_BUILD_STATIC_LIBGCC", False),
            self.define("OMNITRACE_BUILD_STATIC_LIBSTDCXX", False),
            self.define_from_variant("OMNITRACE_BUILD_LTO", "ipo"),
            self.define_from_variant("OMNITRACE_USE_HIP", "rocm"),
            self.define_from_variant("OMNITRACE_USE_MPI", "mpi"),
            self.define_from_variant("OMNITRACE_USE_OMPT", "ompt"),
            self.define_from_variant("OMNITRACE_USE_PAPI", "papi"),
            self.define_from_variant("OMNITRACE_USE_RCCL", "rocm"),
            self.define_from_variant("OMNITRACE_USE_ROCM_SMI", "rocm"),
            self.define_from_variant("OMNITRACE_USE_ROCTRACER", "rocm"),
            self.define_from_variant("OMNITRACE_USE_ROCPROFILER", "rocm"),
            self.define_from_variant("OMNITRACE_USE_PYTHON", "python"),
            self.define_from_variant("OMNITRACE_USE_MPI_HEADERS", "mpi_headers"),
            self.define_from_variant("OMNITRACE_STRIP_LIBRARIES", "strip"),
            self.define_from_variant("OMNITRACE_INSTALL_PERFETTO_TOOLS", "perfetto_tools"),
            # timemory arguments
            self.define("TIMEMORY_UNITY_BUILD", False),
            self.define("TIMEMORY_BUILD_CALIPER", False),
            self.define_from_variant("TIMEMORY_USE_TAU", "tau"),
            self.define_from_variant("TIMEMORY_USE_CALIPER", "caliper"),
        ]

        if "+tau" in spec:
            tau_root = spec["tau"].prefix
            args.append(self.define("TAU_ROOT_DIR", tau_root))

        if "+python" in spec:
            pyexe = spec["python"].command.path
            args.append(self.define("PYTHON_EXECUTABLE", pyexe))
            args.append(self.define("Python3_EXECUTABLE", pyexe))

        if "+mpi" in spec:
            args.append(self.define("MPI_C_COMPILER", spec["mpi"].mpicc))
            args.append(self.define("MPI_CXX_COMPILER", spec["mpi"].mpicxx))

        return args

    def setup_build_environment(self, env):
        if "+tau" in self.spec:
            import glob

            # below is how TAU_MAKEFILE is set in packages/tau/package.py
            pattern = join_path(self.spec["tau"].prefix.lib, "Makefile.*")
            files = glob.glob(pattern)
            if files:
                env.set("TAU_MAKEFILE", files[0])

    def setup_run_environment(self, env):
        if "+python" in self.spec:
            env.prepend_path("PYTHONPATH", join_path(self.prefix.lib, "python", "site-packages"))
