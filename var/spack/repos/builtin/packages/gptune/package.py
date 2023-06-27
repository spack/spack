# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util.lang import memoized

from spack.package import *


class Gptune(CMakePackage):
    """GPTune is an autotuning framework that relies on multitask and transfer
    learnings to help solve the underlying black-box optimization problem using
    Bayesian optimization methodologies."""

    homepage = "https://gptune.lbl.gov/"
    url = "https://github.com/gptune/GPTune/archive/refs/tags/3.0.0.tar.gz"
    git = "https://github.com/gptune/GPTune.git"
    maintainers("liuyangzhuan")

    version("master", branch="master")
    version("4.0.0", sha256="4f954a810d83b73f5abe5b15b79e3ed5b7ebf7bc0ae7335d27b68111bd078102")
    version("3.0.0", sha256="e19bfc3033fff11ff8c20cae65b88b7ca005d2c4e4db047f9f23226126ec92fa")
    version("2.1.0", sha256="737e0a1d83f66531098beafa73dd479f12def576be83b1c7b8ea5f1615d60a53")

    variant("superlu", default=False, description="Build the SuperLU_DIST example")
    variant("hypre", default=False, description="Build the Hypre example")
    variant("mpispawn", default=True, description="MPI spawning-based interface")

    depends_on("mpi", type=("build", "link", "run"))
    depends_on("cmake@3.17:", type="build")
    depends_on("jq", type="run")
    depends_on("blas", type="link")
    depends_on("lapack", type="link")
    depends_on("scalapack", type="link")
    depends_on("py-setuptools", type="build")
    depends_on("py-ipyparallel", type=("build", "run"))
    depends_on("py-numpy@:1.24", type=("build", "run"), when="@:4.0.0")
    depends_on("py-numpy@:1.21.5", type=("build", "run"), when="@:2.1.0")
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-scikit-optimize@master+gptune", type=("build", "run"))
    depends_on("py-gpy", type=("build", "run"))
    depends_on("py-lhsmdu", type=("build", "run"))
    depends_on("py-hpbandster", type=("build", "run"))
    depends_on("py-opentuner", type=("build", "run"))
    depends_on("py-ytopt-autotune@1.1.0", type=("build", "run"))
    depends_on("py-filelock", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-cython", type=("build", "run"))
    depends_on("py-pyaml", type=("build", "run"))
    depends_on("py-statsmodels@0.13.0:", type=("build", "run"))
    depends_on("py-mpi4py@3.0.3:", type=("build", "run"))
    depends_on("pygmo", type=("build", "run"))
    depends_on("openturns", type=("build", "run"))
    depends_on("py-pymoo", type=("build", "run"), when="@3.0.0:")

    depends_on("superlu-dist@develop", when="+superlu", type=("build", "run"))
    depends_on("hypre+gptune@2.19.0", when="+hypre", type=("build", "run"))

    depends_on("openmpi@4:", when="+mpispawn", type=("build", "run"))
    conflicts("mpich", when="+mpispawn")
    conflicts("spectrum-mpi", when="+mpispawn")
    conflicts("cray-mpich", when="+mpispawn")
    conflicts("gcc@:7")

    def cmake_args(self):
        spec = self.spec
        fc_flags = []
        if "%gcc@10:" in spec or self.spec.satisfies("%apple-clang@11:"):
            fc_flags.append("-fallow-argument-mismatch")

        args = [
            "-DGPTUNE_INSTALL_PATH=%s" % python_platlib,
            "-DTPL_BLAS_LIBRARIES=%s" % spec["blas"].libs.joined(";"),
            "-DTPL_LAPACK_LIBRARIES=%s" % spec["lapack"].libs.joined(";"),
            "-DTPL_SCALAPACK_LIBRARIES=%s" % spec["scalapack"].libs.joined(";"),
            "-DCMAKE_Fortran_FLAGS=" + "".join(fc_flags),
            "-DBUILD_SHARED_LIBS=ON",
            "-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx,
            "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
            "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc,
        ]

        return args

    examples_src_dir = "examples"
    env_script = "run_env.sh"
    src_dir = "GPTune"
    nodes = 1
    cores = 4

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run` and generate
        the run environment script."""
        # Generate a custom environment set up script ONCE for the installed
        # software.
        self.write_test_env_sh()

        self.clone_test_examples()

        self.cache_extra_test_sources([self.env_script, self.examples_src_dir])

    def setup_run_environment(self, env):
        env.set("GPTUNE_INSTALL_PATH", python_platlib)

    def write_test_env_sh(self):
        """Generate the post-install test run environment script for
        stand-alone testing."""
        comp_name = self.compiler.name
        comp_version = str(self.compiler.version).replace(".", ",")

        spec = self.spec
        with open(self.env_script, "w") as envfile:
            envfile.write('if [[ $NERSC_HOST = "cori" ]]; then\n')
            envfile.write("    export machine=cori\n")
            envfile.write('elif [[ $(uname -s) = "Darwin" ]]; then\n')
            envfile.write("    export machine=mac\n")
            envfile.write("elif [[ $(dnsdomainname) = " + '"summit.olcf.ornl.gov" ]]; then\n')
            envfile.write("    export machine=summit\n")
            envfile.write(
                'elif [[ $(cat /etc/os-release | grep "PRETTY_NAME") =='
                + ' *"Ubuntu"* || $(cat /etc/os-release | grep'
                + ' "PRETTY_NAME") == *"Debian"* ]]; then\n'
            )
            envfile.write("    export machine=unknownlinux\n")
            envfile.write("fi\n")
            envfile.write("export GPTUNEROOT=$PWD\n")
            mpirun = which(spec["mpi"].prefix.bin.mpirun)
            envfile.write(f"export MPIRUN={mpirun}\n")
            path = join_path(python_platlib, "gptune")
            envfile.write(f"export PYTHONPATH={path}:$PYTHONPATH\n")
            envfile.write("export proc=$(spack arch)\n")
            envfile.write(f"export mpi={spec['mpi'].name}\n")
            envfile.write(f"export compiler={comp_name}\n")
            envfile.write(f"export nodes={self.nodes} \n")
            envfile.write(f"export cores={self.cores} \n")
            envfile.write("export ModuleEnv=$machine-$proc-$mpi-$compiler \n")
            envfile.write(
                'software_json=$(echo ",\\"software_configuration\\":'
                + '{\\"'
                + spec["blas"].name
                + '\\":{\\"version_split\\":'
                + " ["
                + str(spec["blas"].versions).replace(".", ",")
                + ']},\\"'
                + spec["mpi"].name
                + '\\":{\\"version_split\\": ['
                + str(spec["mpi"].versions).replace(".", ",")
                + ']},\\"'
                + spec["scalapack"].name
                + '\\":{\\"version_split\\": ['
                + str(spec["scalapack"].versions).replace(".", ",")
                + ']},\\"'
                + str(comp_name)
                + '\\":{\\"version_split\\": ['
                + str(comp_version)
                + ']}}") \n'
            )
            envfile.write(
                'loadable_software_json=$(echo ",\\"loadable_software_'
                + 'configurations\\":{\\"'
                + spec["blas"].name
                + '\\":{\\"version_split\\": ['
                + str(spec["blas"].versions).replace(".", ",")
                + ']},\\"'
                + spec["mpi"].name
                + '\\":{\\"version_split\\": ['
                + str(spec["mpi"].versions).replace(".", ",")
                + ']},\\"'
                + spec["scalapack"].name
                + '\\":{\\"version_split\\": ['
                + str(spec["scalapack"].versions).replace(".", ",")
                + ']},\\"'
                + str(comp_name)
                + '\\":{\\"version_split\\": ['
                + str(comp_version)
                + ']}}") \n'
            )
            envfile.write(
                'machine_json=$(echo ",\\"machine_configuration\\":'
                + '{\\"machine_name\\":\\"$machine\\",\\"$proc\\":'
                + '{\\"nodes\\":$nodes,\\"cores\\":$cores}}") \n'
            )
            envfile.write(
                'loadable_machine_json=$(echo ",\\"loadable_machine_'
                + 'configurations\\":{\\"$machine\\":{\\"$proc\\":'
                + '{\\"nodes\\":$nodes,\\"cores\\":$cores}}}") \n'
            )

    @property
    def test_src_dir(self):
        return join_path(self.test_suite.current_test_cache_dir, self.examples_src_dir)

    def clone_test_examples(self):
        git = which("git")
        spec = self.spec

        if "+superlu" in spec:
            # copy superlu-dist executables to the correct place
            example_dir = join_path("superlu_dist", "build", "EXAMPLE")
            with working_dir(join_path(self.test_src_dir, "SuperLU_DIST")):
                remove_linked_tree("superlu_dist")

                git("clone", "https://github.com/xiaoyeli/superlu_dist.git")
                mkdirp(example_dir)
                copy("-r", spec["superlu-dist"].prefix.lib.EXAMPLE.pddrive_spawn, example_dir)

        if "+hypre" in spec:
            # copy hypre driver executable to the correct place
            with working_dir(join_path(self.test_src_dir, "Hypre")):
                remove_linked_tree("hypre")

                git("clone", "https://github.com/hypre-space/hypre.git")
                copy("-r", spec["hypre"].prefix.bin.ij, join_path("hypre", "src", "test"))

    @property
    @memoized
    def bash(self):
        return which("bash")

    def test_scalapack_pdgeqrf_rci(self):
        """run Scalapack-PDGEQRF_RCI examples"""
        with working_dir(join_path(self.test_src_dir, "Scalapack-PDGEQRF_RCI")):
            self.bash("run_examples.sh")

    def test_gptune_demo(self):
        """run GPTune-Demo examples"""
        if "+mpispawn" not in self.spec:
            raise SkipTest("Test requires package built with +mpispawn")

        with working_dir(join_path(self.test_src_dir, "GPTune-Demo")):
            self.bash("run_examples.sh")

    def test_scalapack_pdgeqrf(self):
        """run Scalapack-PDGEQRF examples"""
        if "+mpispawn" not in self.spec:
            raise SkipTest("Test requires package built with +mpispawn")

        with working_dir(join_path(self.test_src_dir, "Scalapack-PDGEQRF")):
            self.bash("run_examples.sh")

    def test_scalapack_pdgeqrf_rci(self):
        """run SuperLU_DIST_RCI examples"""
        if "+superlu" not in self.spec:
            raise SkipTest("Test requires package built with +superlu")

        with working_dir(join_path(self.test_src_dir, "SuperLU_DIST_RCI")):
            self.bash("run_examples.sh")

    def test_superlu_dist(self):
        """run SuperLU_DIST examples"""
        if "+superlu+mpispawn" not in self.spec:
            raise SkipTest("Test requires package built with +superlu+mpispawn")

        with working_dir(join_path(self.test_src_dir, "SuperLU_DIST")):
            self.bash("run_examples.sh")

    def test_hypre(self):
        """run Hypre examples"""
        if "+hypre+mpispawn" not in self.spec:
            raise SkipTest("Test requires package built with +hypre+mpispawn")

        with working_dir(join_path(self.test_src_dir, "Hypre")):
            self.bash("run_examples.sh")
