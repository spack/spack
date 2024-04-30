# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.builtin.neuron import Neuron as BuiltinNeuron


class Neuron(BuiltinNeuron):
    __doc__ = BuiltinNeuron.__doc__

    # BBP specific version
    version("develop", branch="master")
    version("9.0.a16", commit="13654b3")
    version("9.0.a15", commit="f64b609")
    version("9.0.a14", commit="bd9426d9")
    version("9.0.a13", commit="3bbdd8da")
    version("9.0.a5", commit="522c866")

    # Patch which reverts 81a7a39 for numerical compatibility for BBP simulations
    patch("revert_Import3d_numerical_format.master.patch", when="@:9.0.a5")

    # Used FastDebug for CI & validation
    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "FastDebug", "RelWithDebInfo", "Release"),
    )

    # Variant for future development
    variant(
        "unified", default=False, description="Enable Unified Memory with GPU build", when="+gpu"
    )

    # reports exit for BBP simulation only
    variant("report", default=True, description="Enable SONATA reports")

    # NMODL optimisations used for benchmarking
    variant(
        "sympyopt",
        default=False,
        description="Use NMODL with SymPy Optimizations",
        when="+coreneuron",
    )

    # enabled in CI
    variant(
        "model_tests",
        default="None",
        description="Enable detailed model tests included in neuron",
        multi=True,
        values=("None", "olfactory", "channel-benchmark", "tqperf-heavy"),
    )

    # used for debugging purposes
    variant(
        "prcellstate",
        default=False,
        description="Enable tracking of voltage and conductivity with prcellstate on CoreNEURON",
    )

    # used during development by core team
    variant(
        "sanitizers",
        default="None",
        description="Enable runtime sanitizers",
        multi=True,
        values=("None", "address", "leak", "undefined"),
    )

    # standard deployment uses submodule to avoid compatibility issues
    depends_on("nmodl", when="+coreneuron")
    depends_on("libsonata-report", when="+report+coreneuron")

    # lazy users do not want to load a compiler module to compile things, and we need a
    # more modern linker
    depends_on("binutils", type="run")

    def cmake_args(self):
        args = super().cmake_args()
        spec = self.spec

        # extra optimisation specific option added
        nmodl_options = ""
        if spec.satisfies("+sympy"):
            nmodl_options += " sympy --analytic"
        if spec.satisfies("+sympyopt"):
            nmodl_options += " --conductance --pade --cse"
        args.append(self.define("CORENRN_NMODL_FLAGS", nmodl_options))

        if spec.satisfies("+tests"):
            # The +tests variant is used in CI pipelines that run the tests
            # directly from the build directory, not via Spack's --test=X
            # option. This overrides the implicit CMake argument that Spack
            # injects. Also, the +tests variant is primarily used for CI pipelines,
            # which do not run on exclusive resources and do not give reliable
            # results for tests that test performance scaling
            args.append(self.define("BUILD_TESTING", True))
            args.append(self.define("NRN_ENABLE_PERFORMANCE_TESTS", False))

        # enable tests to run under CI
        if spec.variants["model_tests"].value != ("None",):
            args.append(
                self.define(
                    "NRN_ENABLE_MODEL_TESTS",
                    ",".join(model for model in spec.variants["model_tests"].value),
                )
            )

        # sanitizers setup during development
        if spec.variants["sanitizers"].value != ("None",):
            if self.compiler.name == "clang":
                args.append(
                    self.define(
                        "LLVM_SYMBOLIZER_PATH",
                        os.path.join(os.path.dirname(self.compiler.cxx), "llvm-symbolizer"),
                    )
                )
            args.append(self.define("NRN_SANITIZERS", ",".join(spec.variants["sanitizers"].value)))

        # Before 9.0.a15 CMake didn't have  build_type=FastDebug
        # If we want to launch BBP CI with such older versions then
        # we should handle FastDebug build type. At least for some
        # time until we are sure that we will be using >=9.0.a15 with
        # FastDebug build type
        if spec.satisfies("@:9.0.a14") and spec.variants["build_type"].value == "FastDebug":
            # moderate optimisation by default
            compilation_flags = ["-g", "-O1"]
            if "%intel" in self.spec:
                # this one definitely seems wise
                compilation_flags += ["-fp-model", "consistent"]
            elif "%oneapi" in self.spec:
                # the documentation doesn't mention consistent for these intel compilers
                compilation_flags.append("-fp-model=precise")

            compilation_flags = " ".join(compilation_flags)
            args.append(self.define("CMAKE_C_FLAGS", compilation_flags))
            args.append(self.define("CMAKE_CXX_FLAGS", compilation_flags))
            args.append(self.define("CMAKE_BUILD_TYPE", "Custom"))

        # Added in https://github.com/neuronsimulator/nrn/pull/1574, this
        # improves ccache performance in CI builds.
        if spec.satisfies("@8.2:"):
            args.append(self.define("NRN_AVOID_ABSOLUTE_PATHS", "ON"))

        dynamic = "ON" if "~gpu" in spec else "OFF"
        args.append(self.define("NRN_ENABLE_MPI_DYNAMIC", dynamic))

        if "+prcellstate" in spec:
            args.append(self.define("CORENRN_ENABLE_PRCELLSTATE", "ON"))

        if spec.satisfies("+coreneuron"):
            args.append(self.define("CORENRN_NMODL_DIR", spec["nmodl"].prefix))
            args.append(self.define_from_variant("CORENRN_ENABLE_REPORTING", "report"))

        if spec.satisfies("+gpu"):
            # instead of assuming that the gcc in $PATH is the right host compiler, take the
            # compiler used to build the cuda package as the CUDA host compiler.
            host_compiler_spec = spec["cuda"].compiler
            # surely this isn't the best way but more robust on different systems
            host_compiler_candidates = [
                c for c in spack.compilers.all_compilers() if c.spec == host_compiler_spec
            ]
            assert len(host_compiler_candidates) == 1
            host_compiler = host_compiler_candidates[0]
            args.append(self.define("CMAKE_CUDA_HOST_COMPILER", host_compiler.cxx))

        return args

    def setup_run_environment(self, env):
        super().setup_run_environment(env)
        # user typically should load necessary C++ compiler before
        # compiling MOD files.
        if self.spec.satisfies("+mpi"):
            env.set("MPICXX_CXX", self.compiler.cxx)

    # TODO: should be removed after neurodamus recipes refactoring
    @property
    def archdir(self):
        """Determine the architecture string from nrnivmodl

        nrnivmodl creates binary in sub-directory like x86_64 or
        aarch64. We need to know this in order to find exact
        paths of binaries.
        """
        args = ["-F=", '$1 == "MODSUBDIR" { print $2; exit; }', str(self.prefix.bin.nrnivmodl)]
        return which("awk")(*args, output=str).strip()
