# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess
import sys

from spack.package import *


class Neuron(CMakePackage):
    """NEURON is a simulation environment for single and networks of neurons.

    NEURON is a simulation environment for modeling individual and networks of
    neurons. NEURON models individual neurons via the use of sections that are
    automatically subdivided into individual compartments, instead of
    requiring the user to manually create compartments. The primary scripting
    language is hoc but a Python interface is also available.
    """

    homepage = "https://www.neuron.yale.edu/"
    url = "http://www.neuron.yale.edu/ftp/neuron/versions/v7.5/nrn-7.5.tar.gz"
    git = "https://github.com/neuronsimulator/nrn"

    # Patch which reverts 81a7a39 for numerical compat
    patch("revert_Import3d_numerical_format.master.patch", when="@7.8.1:")
    # Patch which reverts d9605cb for not hanging on ExperimentalMechComplex
    # Patch for recent CMake versions that don't identify NVHPC as PGI
    patch("patch-v800-cmake-nvhpc.patch", when="@8.0.0%nvhpc^cmake@3.20:")

    version("develop", branch="master")
    version("8.2.2a", commit="eb19ae0")
    version("8.2.1", tag="8.2.1")
    version("8.2.0", tag="8.2.0")
    version("8.1.0", tag="8.1.0")
    version("8.0.2", tag="8.0.2")
    version("8.0.1", tag="8.0.1")
    version("8.0.0", tag="8.0.0")
    version("7.8.1", tag="7.8.1")

    variant("binary",     default=True, description="Create special as a binary instead of shell script (8.0.x and earlier)")
    conflicts("~binary", when='@8.0.999:')
    variant("coreneuron", default=False, description="Enable CoreNEURON support")
    variant("mod-compatibility",  default=True, description="Enable CoreNEURON compatibility for MOD files")
    variant("debug",          default=False, description="Build with flags -g -O0")
    variant("interviews", default=False, description="Enable GUI with INTERVIEWS")
    variant("legacy-fr",  default=True,  description="Use original faraday, R, etc. instead of 2019 nist constants")
    variant("memacs",     default=True,  description="Enable use of memacs")
    variant("mpi",        default=True,  description="Enable MPI parallelism")
    variant("profile",    default=False, description="Enable Tau profiling")
    variant("python",     default=True,  description="Enable python")
    variant("rx3d", default=True, description="Enable cython translated 3-d rxd.")
    variant(
        "sanitizers",
        default="None",
        description="Enable runtime sanitizers",
        multi=True,
        values=("None", "address", "leak", "undefined"),
    )
    variant("tests",      default=False, description="Enable unit tests")
    variant("model_tests", default="None", description="Enable detailed model tests included in neuron", multi=True, values=("None", "olfactory", "channel-benchmark", "tqperf-heavy"))
    variant("legacy-unit", default=True,   description="Enable legacy units")
    variant("caliper", default=False, description="Add LLNL/Caliper support")

    # Build with `ninja` instead of `make`
    generator = 'Ninja'
    depends_on('ninja', type='build')

    depends_on("bison",     type="build")
    depends_on("caliper",   type=("build", "run"), when="+caliper")
    depends_on("flex",      type="build")
    depends_on("pkgconfig", type="build")

    # Readline became incompatible with Mac so we use neuron internal readline.
    # HOWEVER, with the internal version there is a bug which makes
    # Vector.as_numpy() not work!
    depends_on("readline", when=sys.platform != "darwin")

    # Transient dependency
    depends_on("gettext")

    depends_on("mpi",         when="+mpi")
    depends_on("py-mpi4py",   when="+mpi+python+tests")
    depends_on("ncurses")
    depends_on("python@2.6:", when="+python", type=("build", "link", "run"))
    depends_on("py-pytest",   when="+python+tests")
    # Numpy is required for Vector.as_numpy()
    depends_on("py-numpy",    when="+python", type=("build", "run"))
    depends_on("py-cython",   when="+rx3d", type="build")
    depends_on("tau",         when="+profile")
    depends_on("coreneuron+legacy-unit~caliper", when="+coreneuron+legacy-unit~caliper")
    depends_on("coreneuron~legacy-unit~caliper", when="+coreneuron~legacy-unit~caliper")
    depends_on("coreneuron+legacy-unit+caliper", when="+coreneuron+legacy-unit+caliper")
    depends_on("coreneuron~legacy-unit+caliper", when="+coreneuron~legacy-unit+caliper")
    depends_on("py-pytest-cov", when="+tests@8:")

    conflicts("+rx3d",    when="~python")

    # ==============================================
    # ==== CMake build system related functions ====
    # ==============================================
    def cmake_args(self):
        def cmake_enable_option(spec_requiremement):
            value = "TRUE" if spec_requiremement in self.spec else "FALSE"
            cmake_name = spec_requiremement[1:].upper().replace("-", "_")
            return "-DNRN_ENABLE_" + cmake_name + ":BOOL=" + value
        args = [cmake_enable_option(variant) for variant in ["+interviews",
                                                             "+legacy-fr",
                                                             "+python",
                                                             "+memacs",
                                                             "+rx3d",
                                                             "+coreneuron",
                                                             "+tests"]]
        compilation_flags = []
        if self.spec.variants['model_tests'].value != ("None",):
            args.append('-DNRN_ENABLE_MODEL_TESTS=' + ",".join(
                model for model in self.spec.variants["model_tests"].value))
        if self.spec.variants["sanitizers"].value != ("None",):
            if self.compiler.name == "clang":
                args.append(
                    "-DLLVM_SYMBOLIZER_PATH="
                    + os.path.join(
                        os.path.dirname(self.compiler.cxx), "llvm-symbolizer"
                    )
                )
            args.append(
                "-DNRN_SANITIZERS=" + ",".join(self.spec.variants["sanitizers"].value)
            )
        if "+mpi" in self.spec:
            args.append("-DNRN_ENABLE_MPI=ON")
            if "~coreneuron" in self.spec:
                args.append("-DNRN_ENABLE_MPI_DYNAMIC=ON")
        else:
            args.append("-DNRN_ENABLE_MPI=OFF")
        if "+python" in self.spec:
            args.append("-DPYTHON_EXECUTABLE:FILEPATH="
                        + self.spec["python"].command.path)
        if "+debug" in self.spec:
            compilation_flags += ['-g', '-O0']
            # Remove default flags (RelWithDebInfo etc.)
            args.append("-DCMAKE_BUILD_TYPE=Custom")
        if "+mod-compatibility" in self.spec:
            args.append("-DNRN_ENABLE_MOD_COMPATIBILITY:BOOL=ON")
        if "+binary" in self.spec and '@:8.0.999' in self.spec:
            args.append("-DNRN_ENABLE_BINARY_SPECIAL=ON")
        if "+legacy-unit" in self.spec:
            args.append('-DNRN_DYNAMIC_UNITS_USE_LEGACY=ON')
        if "+coreneuron" in self.spec:
            args.append('-DCORENEURON_DIR=' + self.spec["coreneuron"].prefix)
        # NVHPC 21.11 and newer detect ABM support and define __ABM__, which
        # breaks Random123 compilation. NEURON inserts a workaround for this in
        # https://github.com/neuronsimulator/nrn/pull/1587.
        if self.spec.satisfies('@:8.0.999%nvhpc@21.11:'):
            compilation_flags.append('-DR123_USE_INTRIN_H=0')
        # Added in https://github.com/neuronsimulator/nrn/pull/1574, this
        # improves ccache performance in CI builds.
        if self.spec.satisfies("@8.2:"):
            args.append("-DNRN_AVOID_ABSOLUTE_PATHS=ON")
        # Pass Spack's target architecture flags in explicitly so that they're
        # saved to the nrnivmodl Makefile.
        compilation_flags.append(
            self.spec.architecture.target.optimization_flags(self.spec.compiler)
        )
        compilation_flags = ' '.join(compilation_flags)
        args.append("-DCMAKE_C_FLAGS=" + compilation_flags)
        args.append("-DCMAKE_CXX_FLAGS=" + compilation_flags)
        if "+caliper" in self.spec:
            args.append('-DNRN_ENABLE_PROFILING=ON')
            args.append('-DNRN_PROFILER=caliper')
        return args

    # Create symlink in share/nrn/lib for the python libraries
    # which is the place that neuron expects the library similarly
    # to autotools installation
    # See : https://github.com/neuronsimulator/nrn/issues/567
    @run_after("install")
    def symlink_python_lib(self):
        if "+python" in self.spec:
            os.symlink(self.prefix.lib.python,
                       self.prefix.share.nrn.lib.python)

    # ==============================================
    # ============== Common functions ==============
    # ==============================================
    @property
    def archdir(self):
        """Determine the architecture neuron build architecture.

        With cmake get the architecture of the system from spack.
        With autotools instead of recreating the logic of the
        neuron"s configure we dynamically find the architecture-
        specific directory by looking for a specific binary.
        """
        return subprocess.Popen(
            ['awk', '-F=', '$1 == "MODSUBDIR" { print $2; exit; }',
             str(self.prefix.bin.nrnivmodl)],
            stdout=subprocess.PIPE
        ).communicate()[0].decode().strip()

    @run_after("install")
    def filter_compilers(self):
        """run after install to avoid spack compiler wrappers
        getting embded into nrnivmodl script"""

        cc_compiler = self.compiler.cc
        cxx_compiler = self.compiler.cxx
        if self.spec.satisfies("+mpi"):
            cc_compiler = self.spec["mpi"].mpicc
            cxx_compiler = self.spec["mpi"].mpicxx

        nrnmech_makefile = join_path(self.prefix,
                                     "bin/nrnmech_makefile")

        kwargs = {"backup": False, "string": True}

        # The assign_operator should follow any changes done in
        # "bin/nrnivmodl_makefile_cmake.in" and "bin/nrnmech_makefile.in"
        # when assigning CC and CXX variables
        if self.spec.satisfies("@:7.99"):
            assign_operator = "?="
        else:
            assign_operator = "="

        filter_file("CC {0} {1}".format(assign_operator, env["CC"]),
                    "CC = {0}".format(cc_compiler),
                    nrnmech_makefile,
                    **kwargs)
        filter_file("CXX {0} {1}".format(assign_operator, env["CXX"]),
                    "CXX = {0}".format(cxx_compiler),
                    nrnmech_makefile,
                    **kwargs)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", join_path(self.prefix, "bin"))
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "lib"))
        if self.spec.satisfies("+mpi"):
            env.set("MPICC_CC", self.compiler.cc)
            env.set("MPICXX_CXX", self.compiler.cxx)
        if self.spec.satisfies("+python"):
            env.prepend_path("PYTHONPATH", self.spec.prefix.lib.python)

    def setup_dependent_package(self, module, dependent_spec):
        dependent_spec.package.neuron_basedir = self.prefix
        dependent_spec.package.nrnivmodl_outdir = self.archdir
