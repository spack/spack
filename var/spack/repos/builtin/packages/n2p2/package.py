# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class N2p2(MakefilePackage):
    """N2p2 (The neural network potential package) provides ready-to-use
    software for high-dimensional neural network potentials
    in computational physics and chemistry."""

    homepage = "https://github.com/CompPhysVienna/n2p2"
    url = "https://github.com/CompPhysVienna/n2p2/archive/v2.1.0.tar.gz"

    license("GPL-3.0-only")

    version("2.2.0", sha256="4acaa255632a7b9811d7530fd52ac7dd0bb3a8e3a3cf8512beadd29b62c1bfef")
    version("2.1.4", sha256="f1672c09af4ed16a7f396606977e4675a0fee98f04bfd9574907fba4b83a14ef")
    version("2.1.1", sha256="90fbc0756132984d0d7e6d92d2f53358c120e75f148910d90c027158163251b9")
    version("2.1.0", sha256="283c00e9a5b964f4c84a70c5f1cef7167e9b881080b50a221da08799e5ede400")

    variant("doc", default=False, description="build documentation with Doxygen")
    variant("shared", default=False, description="build shared libraries")

    patch("interface-makefile.patch", when="@2.1.0")
    patch("interface-makefile211.patch", when="@2.1.1:")
    patch("libnnp-makefile.patch", when="@:2.1.1")
    patch("libnnp-makefile212.patch", when="@2.1.2:2.1.4")
    patch("nnp_test.h.patch")

    depends_on("mpi")
    depends_on("blas")
    depends_on("gsl", type=("build", "run", "link"))
    depends_on("eigen", type=("build", "run", "link"))
    depends_on("doxygen", type="build", when="+doc")
    depends_on("texlive", type="build", when="+doc")
    depends_on("py-cython", type=("build", "run"))
    depends_on("py-breathe", type="build", when="+doc")
    depends_on("py-sphinx", type="build", when="+doc")
    depends_on("py-sphinx-rtd-theme", type="build", when="+doc")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, type="link")
    depends_on("lcov", type=("build", "run"))
    depends_on("py-pytest", type=("build", "run"))
    depends_on("py-pytest-cov", type="run")
    depends_on("py-coverage@4.5.4", type="run")
    depends_on("py-packaging", type="run")
    depends_on("python", type=("build", "run"))

    test_requires_compiler = True

    def edit(self, spec, prefix):
        makefile = FileFilter(join_path("src", "makefile"))
        makefile.filter("MODE=.*", f"MODE={'shared' if '+shared' in spec else 'static'}")

        makefile = FileFilter(join_path("src", "makefile.gnu"))
        blas_libs = self.spec["blas"].libs
        makefile.filter("PROJECT_CC=.*", f"PROJECT_CC={spack_cxx}")
        makefile.filter("PROJECT_MPICC=.*", f"PROJECT_MPICC={self.spec['mpi'].mpicxx}")
        makefile.filter("PROJECT_CFLAGS=.*", f"PROJECT_CFLAGS={self.compiler.cxx11_flag}")
        makefile.filter(
            "PROJECT_LDFLAGS_BLAS.*", f"PROJECT_LDFLAGS_BLAS={blas_libs.ld_flags} -lgsl -lgslcblas"
        )

    def build(self, spec, prefix):
        with working_dir("src"):
            # Add --no-print-directory flag to avoid issues when variables set
            # to value of shell function with cd cmd used as target (see #43192)
            make("--no-print-directory")
            make("--no-print-directory", "lammps-nnp")
            make("--no-print-directory", "pynnp")
            if "+doc" in self.spec:
                make("--no-print-directory", "doc")

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        if "+doc" in self.spec:
            install_tree("doc", prefix.doc)
        install_tree("examples", prefix.examples)
        install_tree("include", prefix.include)
        install_tree("lib", prefix.lib)
        install_tree("tools", prefix.tools)

    @run_after("install")
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self)

    def test_n2p2(self):
        """Run benchmark tests"""
        with working_dir(join_path(self.install_test_root, "test"), create=False):
            make("clean")

        with working_dir(join_path(self.install_test_root, "src"), create=False):
            make("clean")
            make(
                "MODE=test",
                f"PROJECT_GSL={self.spec['gsl'].prefix.include}",
                f"PROJECT_EIGEN={self.spec['eigen'].prefix.include.eigen3}",
            )
            make(
                "MODE=test",
                "lammps-nnp",
                f"PROJECT_GSL={self.spec['gsl'].prefix.include}",
                f"PROJECT_EIGEN={self.spec['eigen'].prefix.include.eigen3}",
            )
            make("pynnp", "MODE=test")

        with working_dir(join_path(self.install_test_root, "test"), create=False):
            if self.spec.satisfies("%fj"):
                f = FileFilter(join_path("cpp", "nnp_test.h"))
                mpirun = self.spec["mpi"].prefix.bin.mpirun
                f.filter("(example.co", f'("{mpirun} -n 1 " + example.co', string=True)

            f = FileFilter(join_path("cpp", "makefile"))
            f.filter("log_level=.*", "log_level=$(LOG_LEVEL) 2>&1 | tee -a ../output_cpp.txt")

            f = FileFilter(join_path("python", "makefile"))
            f.filter("term\\s-v.*", "term -v | tee -a ../output_python.txt")

            make("cpp", parallel=False)
            make("python", parallel=False)

            test_dir = self.test_suite.current_test_data_dir
            expected_file = join_path(test_dir, f"expected-result-{self.version}.txt")
            check_n2p2 = Executable(join_path(test_dir, "result-check.sh"))
            check_n2p2("./output_cpp.txt", "./output_python.txt", expected_file)
