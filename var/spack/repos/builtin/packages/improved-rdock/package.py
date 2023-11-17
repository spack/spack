# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class ImprovedRdock(MakefilePackage):
    """Improved version of rDock.
    rDock is a fast and versatile Open Source docking program
    that can be used to dock small molecules against proteins and
    nucleic acids.
    The original version is found at the following URL:
    https://sourceforge.net/projects/rdock/files/rDock_2013.1_src.tar.gz
    """

    homepage = "https://github.com/clinfo/improved_rDock"
    git = "https://github.com/clinfo/improved_rDock.git"

    version("main", branch="main")

    depends_on("popt")
    depends_on("cppunit")
    depends_on("openbabel @3.0.0: +python", type="run")
    depends_on("py-numpy", type="run")
    depends_on("mpi")

    patch("rdock_ld.patch")
    patch("rdock_python3.patch", when="^python@3:")
    patch("rdock_newcxx.patch")
    patch("rdock_useint.patch")
    patch("rdock_erase.patch")
    patch("rdock_loop.patch", when="target=aarch64:")
    patch("rdock_const.patch", when="%fj")
    patch("rdock_const2.patch", when="%fj")

    def edit(self, spec, prefix):
        # compiler path
        tm = FileFilter(join_path("build", "tmakelib", "linux-g++-64", "tmake.conf"))
        tm.filter("/usr/bin/gcc", spack_cc)
        tm.filter("mpicxx", self.spec["mpi"].mpicxx)
        # compiler option
        if self.spec.target.family == "aarch64":
            tm.filter("-m64", "")
        if not self.spec.satisfies("%gcc"):
            tm.filter("-pipe", "")

    def build(self, spec, prefix):
        with working_dir("build"):
            make("linux-g++-64")

    def install(self, spec, prefix):
        for shfile in find("bin", "*"):
            set_executable(shfile)
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        env.set("RBT_ROOT", self.prefix)

    def test_rbcavity_help(self):
        """Check ability to run rbcavity."""
        rbcavity = Executable(self.prefix.bin.rbcavity)
        out = rbcavity("--help", output=str.split, error=str.split)
        expected = ["Usage:", "Help options"]
        check_outputs(expected, out)

    def test_rbdock_help(self):
        """Check ability to run rbdock."""
        rbdock = Executable(self.prefix.bin.rbdock)
        out = rbdock("--help", output=str.split, error=str.split)
        expected = ["Usage:", "Help options"]
        check_outputs(expected, out)

    def test_1sj0(self):
        """run tests against the 1sj0 example"""
        # Since need data and examples copied, need to move down a level
        work_dir = "run_tests"
        mkdirp(work_dir)

        # First copy the relevant example and data files for use in the series
        #  of tests.
        copy(join_path(self.prefix.example, "1sj0", "*"), work_dir)
        install_tree(self.prefix.data, join_path(work_dir, "data"))

        rdock = join_path(".", "1sj0_rdock.prm")
        dock = join_path(".", "dock.prm")
        legand = join_path(".", "1sj0_ligand.sd")

        # TODO: This test does not appear to work outside the installation
        # TODO: directory and needs package developer/user expertise to fix.
        # TODO: At present the program core dumps when manually repeat the
        # TODO: test test command.
        # with test_part(self, "test_1sj0_rbcavity", purpose="run rbcavity", work_dir=work_dir):
        #     rbcavity = Executable(self.prefix.bin.rbcavity)
        #     opts = ["-r", rdock, "-was"]
        #     rbcavity(*opts)

        # TODO: This test appears to pass but actually fails without an error
        # TODO: code but proc0.out has an RBT_FILE_READ_ERROR failure looking
        # TODO: for a file.
        # with test_part(self, "test_1sj0_rbdock", purpose="run rbdock", work_dir=work_dir):
        #     mpirun = Executable(self.spec["mpi"].prefix.bin.mpirun)
        #     opts = [
        #         "-n",
        #         "1",
        #         self.prefix.bin.rbdock,
        #         "-r",
        #         rdock,
        #         "-p",
        #         dock,
        #         "-n",
        #         "10",
        #         "-i",
        #         legand,
        #         "-o",
        #         "1sj0_docking_out",
        #         "-s",
        #         "1",
        #     ]
        #     mpirun(*opts)

        # TODO: This test appears to pass but actually fails without an error
        # TODO: code. The failure is in "Can't open ./1sj0_docking_out.sd: No
        # TODO: such file or directory at $PREFIX/lib/SDRecord.pm line 50"
        # with test_part(self, "test_1sj0_test_script", purpose="run test.sh", work_dir=work_dir):
        #     bash = which("bash")
        #     bash(join_path(self.test_suite.current_test_data_dir, "test.sh"))

        # TODO: This test fails with no data reported in the columns and it
        # TODO: is dependent on the results from the above test
        # with test_part(self, "test_1sj0_sdrmsd", purpose="run sdrmsd", work_dir=work_dir):
        #     python = self.spec["python"].command
        #     opts = [self.prefix.bin.sdrmsd, legand, join_path(".", "1sj0_docking_out_sorted.sd")]
        #     out = python(*opts, output=str.split, error=str.split)
        #     expected = [r"1\t0.55", r"100\t7.91"]
        #     check_outputs(expected, out)
