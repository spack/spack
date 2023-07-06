# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Steps(CMakePackage):
    """STochastic Engine for Pathway Simulation"""

    homepage = "https://groups.oist.jp/cnu/software"
    git = "https://github.com/CNS-OIST/STEPS.git"

    maintainers("tristan0x")

    version("develop", branch="master", submodules=True)
    version("4.1.1", submodules=True)

    variant(
        "codechecks",
        default=False,
        description="Perform additional code checks like code formatting or static analysis",
    )
    variant("lapack", default=False, description="Use new BDSystem/Lapack code for E-Field solver")
    variant(
        "distmesh", default=True, when="+mpi", description="Add solvers based on distributed mesh"
    )
    variant("petsc", default=True, description="Use PETSc library for parallel E-Field solver")
    variant("mpi", default=True, description="Use MPI for parallel solvers")
    variant("coverage", default=False, description="Enable code coverage")
    variant("bundle", default=False, description="Use bundled libraries")
    variant("stochtests", default=True, description="Add stochastic tests to ctests")
    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel", "RelWithDebInfoAndAssert"),
    )
    variant(
        "caliper", default=False, description="Build in caliper support (Instrumentor Interface)"
    )
    variant(
        "likwid", default=False, description="Build in likwid support (Instrumentor Interface)"
    )

    # Build with `ninja` instead of `make`
    generator("ninja")

    depends_on("benchmark", type=("build", "test"))
    depends_on("blas")
    depends_on("boost", type="build")
    depends_on("caliper", when="+caliper")
    depends_on("easyloggingpp", when="~bundle")
    depends_on("gmsh", when="+distmesh")
    depends_on("lapack", when="+lapack")
    depends_on("lcov", when="+coverage", type="build")
    depends_on("likwid", when="+likwid")
    depends_on("metis+int64")
    depends_on("mpi", when="+mpi")
    depends_on("omega-h+gmsh+mpi", when="~bundle+distmesh")
    depends_on("petsc~debug+int64+mpi", when="+petsc+mpi")
    depends_on("petsc~debug+int64~mpi", when="+petsc~mpi")
    depends_on("pkgconfig", type="build")
    depends_on("py-cython")
    depends_on("py-gcovr", when="+coverage", type="build")
    depends_on("py-h5py", type=("build", "test", "run"))
    depends_on("py-matplotlib", type=("build", "test"))
    depends_on("py-mpi4py", when="+distmesh", type=("build", "test", "run"))
    depends_on("py-numpy", type=("build", "test", "run"))
    depends_on("py-scipy", type=("build", "test", "run"))
    depends_on("python", type=("build", "test", "run"))
    depends_on("random123", when="~bundle")
    depends_on("sundials@:2.99.99+int64", when="~bundle")

    patch("for_aarch64.patch", when="target=aarch64:")

    def patch(self):
        # easylogging requires compilation by
        # its dependents: splice in disabling all errors
        filter_file(r"(-Wno-double-promotion)", r"-Wno-error \1", "src/steps/util/CMakeLists.txt")

    def cmake_args(self):
        args = [
            self.define("BLAS_LIBRARIES", self.spec["blas"].libs.joined(";")),
            self.define("PYTHON_EXECUTABLE", self.spec["python"].command),
            self.define("STEPS_INSTALL_PYTHON_DEPS", False),
            self.define_from_variant("BUILD_STOCHASTIC_TESTS", "stochtests"),
            self.define_from_variant("BUILD_TESTING", "codechecks"),
            self.define_from_variant("ENABLE_CODECOVERAGE", "coverage"),
            self.define_from_variant("STEPS_ENABLE_ERROR_ON_WARNING", "codechecks"),
            self.define_from_variant("STEPS_TEST_FORMATTING", "codechecks"),
            self.define_from_variant("STEPS_USE_CALIPER_PROFILING", "caliper"),
            self.define_from_variant("STEPS_USE_DIST_MESH", "distmesh"),
            self.define_from_variant("STEPS_USE_LIKWID_PROFILING", "likwid"),
            self.define_from_variant("USE_BDSYSTEM_LAPACK", "lapack"),
            self.define_from_variant("USE_MPI", "mpi"),
            self.define_from_variant("USE_PETSC", "petsc"),
        ]

        args.extend(
            [
                self.define_from_variant(f"USE_BUNDLE_{bundle}", "bundle")
                for bundle in ["EASYLOGGINGPP", "OMEGA_H", "RANDOM123", "SUNDIALS", "SUPERLU_DIST"]
            ]
        )

        return args

    @property
    def build_targets(self):
        targets = []
        if "+coverage" in self.spec:
            if self.compiler.name != "gcc":
                raise ValueError(
                    "Package " + self.name + " build with coverage enabled requires GCC to build"
                )
            targets = [
                "CTEST_OUTPUT_ON_FAILURE=1",
                "all",  # build
                "coverage_init",  # initialize coverage counters
                "test",  # run tests suite
                "coverage",  # collect coverage counters and build reports
            ]
        return targets

    def setup_run_environment(self, env):
        # This recipe exposes a Python package from a C++ CMake project.
        # This hook is required to reproduce what Spack PythonPackage does.
        env.prepend_path("PYTHONPATH", self.prefix)
