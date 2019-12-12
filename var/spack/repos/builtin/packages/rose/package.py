# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# -----------------------------------------------------------------------------
# Author: Justin Too, Nathan Pinnow
# -----------------------------------------------------------------------------

from spack import *


class Rose(AutotoolsPackage):
    """A compiler infrastructure to build source-to-source program
       transformation and analysis tools.
       (Developed at Lawrence Livermore National Lab)"""

    homepage = "http://rosecompiler.org/"
    url = "https://github.com/rose-compiler/rose/archive/v0.9.12.45.zip"
    git = "https://github.com/rose-compiler/rose.git"

    # --------------------------------------------------------------------------
    # ROSE Versions
    # --------------------------------------------------------------------------
    # 
    version("0.9.12.45", sha256="1c6768b8df2e4bcb9608ff5f0d15a56c237c37092968cadbef7294fa1d5256ae")
    
    #Version for edg binary is found in src/frontend/CxxFrontend/EDG_VERSION and may be different then ROSE_VERSION
    resource(name="roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-4.9-5.0.9.12.45.tar.gz",
             expand=False,
             placement="rose-build/src/frontend/CxxFrontend/",
             when="@0.9.12.45 %gcc@4.9.0:4.9.99",
             url="http://edg-binaries.rosecompiler.org/roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-4.9-5.0.9.12.45.tar.gz",
             sha256="859330f70e58900dc3a6be294250de1868dfc853cd65e1d8e906c9b0134cc22a")

    resource(name="roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-5-5.0.9.12.45.tar.gz",
             expand=False,
             placement="rose-build/src/frontend/CxxFrontend/",
             when="@0.9.12.45 %gcc@5.0:5.99",
             url="http://edg-binaries.rosecompiler.org/roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-5-5.0.9.12.45.tar.gz",
             sha256="822add985b8364d0ea81bf57786c73b6d89f7583f6765e556036a89ce8cfdfb8")
    
    resource(name="roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-6-5.0.9.12.45.tar.gz",
             expand=False,
             placement="rose-build/src/frontend/CxxFrontend/",
             when="@0.9.12.45 %gcc@6.0:6.99",
             url="http://edg-binaries.rosecompiler.org/roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-6-5.0.9.12.45.tar.gz",
             sha256="45222ad510bf8350f1e0cb6945cb22646804e82b23dfffa4f11ff96d082323e7")

    resource(name="roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-7-5.0.9.12.45.tar.gz",
             expand=False,
             placement="rose-build/src/frontend/CxxFrontend/",
             when="@0.9.12.45 %gcc@7.0:7.99",
             url="http://edg-binaries.rosecompiler.org/roseBinaryEDG-5-0-x86_64-pc-linux-gnu-gnu-7-5.0.9.12.45.tar.gz",
             sha256="feb318b186919734de952bf3302c19a44f1d4c759cd0abaf554adc074b82ab03")

    # git versions depends on internet connection at build time
    version("develop", branch="develop")

    # --------------------------------------------------------------------------
    # Dependencies
    # --------------------------------------------------------------------------
    depends_on("autoconf@2.69:", type="build")
    depends_on("automake@1.14:", type="build")
    depends_on("libtool@2.4:", type="build")

    # C++11 compatible boost and gcc versions required for +cxx11 variant:
    depends_on("boost@1.60.0:1.64.0,1.65.1,1.66.0:1.67.0 cxxstd=11", when="+cxx11")
    depends_on("boost@1.60.0:1.64.0,1.65.1,1.66.0:1.67.0",           when="~cxx11")

    # --------------------------------------------------------------------------
    # Variants
    # --------------------------------------------------------------------------
    variant("debug", default=False, description="Enable compiler debugging symbols")
    variant("optimized", default=False, description="Enable compiler optimizations")

    variant("tests", default=False, description="Build the tests directory")
    variant("tutorial", default=False, description="Build the tutorial directory")

    variant("tools", default=False, description="Build a selection of ROSE based tools")

    variant(
        "mvapich2_backend",
        default=False,
        description="Enable mvapich2 backend compiler",
    )
    depends_on("mvapich2", when="+mvapich2_backend")

    variant("binanalysis", default=False, description="Enable binary analysis tooling")
    depends_on("libgcrypt", when="+binanalysis", type="build")
    depends_on("py-binwalk", when="+binanalysis", type="run")

    variant("c", default=True, description="Enable c language support")
    variant("cxx", default=True, description="Enable c++ language support")

    # Use spack install cxxflags=-std=c++11
    variant("cxx11", default=True, description="Enable c++11 language support")

    variant("fortran", default=False, description="Enable fortran language support")
    depends_on("jdk", when="+fortran")

    variant("z3", default=False, description="Enable z3 theorem prover")
    depends_on("z3", when="+z3")

    variant(
        "edg_source",
        default=False,
        description="Use the EDG C/C++ frontend source code",
    )
    depends_on("git", when="+edg_source")

    # ------------------------------------------------------------------------
    # ROSE-based Projects
    # ------------------------------------------------------------------------
    variant("codethorn", default=False, description="Enable the CodeThorn project")
    variant(
        "autopar",
        default=False,
        description="Enable the autoParallelization project"
    )
    variant("polyopt", default=False, description="Enable the PolyOpt project")

    build_directory = "rose-build"

    def autoreconf(self, spec, prefix):
        with working_dir(self.stage.source_path):
            bash = which("bash")
            bash("build")

        if "+edg_source" in spec:
            git = which("git")
            git(
                "clone",
                "rose-dev@rosecompiler1.llnl.gov:rose/edg4x/edg.git",
                "src/frontend/CxxFrontend/EDG",
            )

    @property
    def languages(self):
        spec = self.spec
        langs = [
            "binaries" if "+binanalysis" in spec else "",
            "c" if "+c" in spec else "",
            "c++" if "+cxx" in spec else "",
            "fortran" if "+fortran" in spec else "",
        ]
        return list(filter(None, langs))

    def configure_args(self):
        spec = self.spec

        if "+mvapich2_backend" in spec:
            cc = spec["mvapich2"].mpicc
            cxx = spec["mvapich2"].mpicxx
        else:
            cc = spack_cc
            cxx = spack_cxx

        args = [
            "--disable-boost-version-check",
            "--with-alternate_backend_C_compiler={0}".format(cc),
            "--with-alternate_backend_Cxx_compiler={0}".format(cxx),
            "--with-boost={0}".format(spec["boost"].prefix),
            "--enable-languages={0}".format(",".join(self.languages)),
        ]

        if "+z3" in spec:
            args.append("--with-z3={0}".format(spec["z3"].prefix))
        else:
            args.append("--without-z3")

        if "+tests" in spec:
            args.append("--enable-tests-directory")
        else:
            args.append("--disable-tests-directory")

        if "+tutorial" in spec:
            args.append("--enable-tutorial-directory")
        else:
            args.append("--disable-tutorial-directory")

        if "+fortran" in spec:
            args.append("--with-java={0}".format(spec["jdk"].prefix))
        else:
            args.append("--without-java")

        if "+debug" in spec:
            args.append("--with-CXX_DEBUG=-g")
        else:
            args.append("--without-CXX_DEBUG")

        if "+optimized" in spec:
            args.append("--with-C_OPTIMIZE=-O0")
            args.append("--with-CXX_OPTIMIZE=-O0")
        else:
            args.append("--without-C_OPTIMIZE")
            args.append("--without-CXX_OPTIMIZE")

        if "+cxx11" in spec:
            args.append("CXXFLAGS=-std=c++11")

        return args

    def setup_build_environment(self, env):
        if "+codethorn" in self.spec:
            env.set("CXXFLAGS", "-std=c++11")

    def build(self, spec, prefix):
        # Spack will automatically pass ncpus as the number of make jobs.
        #
        # If you really want to srun this on a separate node, you can do this:
        #
        #   $ srun -n1 spack install rose
        #
        with working_dir(self.build_directory):

            # Compile librose
            make("core")

            if "+tools" in spec:
                make("tools")

            # -----------------------------------------------------------------
            # ROSE-based Projects
            # -----------------------------------------------------------------
            if "+codethorn" in spec:
                with working_dir("projects/CodeThorn"):
                    make()

            if "+autopar" in spec:
                with working_dir("projects/autoParallelization"):
                    make()

            if "+polyopt" in spec:
                mkdir = which("mkdir")
                mkdir("-p", "projects/PolyOpt2")
                with working_dir("projects/PolyOpt2"):
                    env["ROSE_SRC"] = self.stage.source_path
                    env["ROSE_ROOT"] = self.prefix

                    bash = which("bash")
                    bash(join_path(self.stage.source_path, "projects/PolyOpt2/install.sh"))

    def install(self, spec, prefix):
        with working_dir(self.build_directory):

            # Compile and Install librose
            make("install-core")

            if "+tools" in spec:
                make("install-tools")

            # -----------------------------------------------------------------
            # ROSE-based Projects
            # -----------------------------------------------------------------
            if "+codethorn" in spec:
                with working_dir("projects/CodeThorn"):
                    make("install")

            if "+autopar" in spec:
                with working_dir("projects/autoParallelization"):
                    make("install")
