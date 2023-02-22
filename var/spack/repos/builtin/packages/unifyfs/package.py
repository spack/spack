# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Unifyfs(AutotoolsPackage):
    """User level file system that enables applications to use node-local
    storage as burst buffers for shared files. Supports scalable and efficient
    aggregation of I/O bandwidth from burst buffers while having the same life
    cycle as a batch-submitted job.
    UnifyFS is designed to support common I/O workloads, including
    checkpoint/restart. While primarily designed for N-N write/read, UnifyFS
    compliments its functionality with the support for N-1 write/read."""

    homepage = "https://github.com/LLNL/UnifyFS"
    git = "https://github.com/LLNL/UnifyFS.git"
    url = "https://github.com/LLNL/UnifyFS/releases/download/v0.9.2/unifyfs-0.9.2.tar.gz"
    maintainers("CamStan")

    tags = ["e4s"]

    version("develop", branch="dev")
    version("1.0.1", sha256="d92800778661b15ab50275c4efe345a6c60d8f1802a0d5909fda38db91b12116")
    version("1.0", sha256="c9ad0d15d382773841a3dab89c661fbdcfd686ec37fa263eb22713f6404258f5")
    version(
        "0.9.2",
        sha256="7046625dc0677535f5d960187cb2e2d58a6f8cfb4dc6a3604f825257eb0891aa",
        deprecated=True,
    )
    version(
        "0.9.1",
        sha256="2498a859cfa4961356fdf5c4c17e3afc3de7e034ad013b8c7145a622ef6199a0",
        deprecated=True,
    )

    variant(
        "auto-mount",
        default="True",
        description="Enable automatic mount/unmount in MPI_Init/Finalize",
    )
    variant(
        "boostsys",
        default="False",
        description="Have Mercury use preprocessor headers from boost dependency",
    )
    variant("fortran", default="True", description="Build with gfortran support")
    variant("pmi", default="False", description="Enable PMI2 build options")
    variant("pmix", default="False", description="Enable PMIx build options")
    variant(
        "preload",
        default="False",
        when="@1.0.1:",
        description="Enable support for LD_PRELOAD library",
    )
    variant("spath", default="True", description="Use spath library to normalize relative paths")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("automake@1.15:", type="build", when="@0.9.2:")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    # Required dependencies
    depends_on("gotcha@1.0.4:")
    depends_on("mochi-margo@0.4.3", when="@:0.9.1")
    depends_on("mochi-margo@0.9.6", when="@0.9.2:1.0")
    depends_on("mochi-margo@0.9.6:0.9.9", when="@develop")
    depends_on("mpi")
    depends_on("openssl@:1")

    # Mochi-Margo dependencies
    depends_on("mercury@1.0.1+bmi", when="@:0.9.1")
    depends_on("mercury@2.1", when="^mochi-margo@0.9.6:0.9.9")
    depends_on("mercury~boostsys", when="~boostsys")
    depends_on("libfabric fabrics=rxm,sockets,tcp", when="^mercury@2:+ofi")

    # Optional dependencies
    depends_on("spath~mpi", when="+spath")

    conflicts("^libfabric@1.13")
    conflicts("^mercury~bmi~ofi")
    conflicts("^mercury~sm")
    # Known compatibility issues with ifort and xlf. Fixes coming.
    conflicts("%intel", when="+fortran")
    conflicts("%xl", when="+fortran")

    patch("unifyfs-sysio.c.patch", when="@0.9.1")
    patch("include-sys-sysmacros.h.patch", when="@0.9.1:0.9.2")

    # Parallel disabled to prevent tests from being run out-of-order when
    # installed with the --test={root, all} option.
    parallel = False
    debug_build = False
    build_directory = "spack-build"

    # Only builds properly with debug symbols when flag_handler =
    # build_system_flags.
    # Override the default behavior in order to set debug_build which is used
    # to set the --disable-silent-rules option when configuring.
    def flag_handler(self, name, flags):
        if name in ("cflags", "cppflags"):
            if "-g" in flags:
                self.debug_build = True
        if name == "cflags":
            if self.spec.satisfies("%oneapi@2022.2.0:"):
                flags.append("-Wno-error=deprecated-non-prototype")
                flags.append("-Wno-error=unused-function")
            if self.spec.satisfies("%gcc@4"):
                flags.append("-std=gnu99")
        return (None, None, flags)

    def setup_build_environment(self, env):
        # GCC11 generates a bogus array bounds error:
        # See https://gcc.gnu.org/bugzilla/show_bug.cgi?id=98266
        if "%gcc@11" in self.spec:
            env.append_flags("CFLAGS", "-Wno-array-bounds")
        if self.spec.satisfies("%oneapi"):
            env.append_flags("CFLAGS", "-Wno-unused-function")

    def configure_args(self):
        spec = self.spec
        args = ["--with-gotcha=%s" % spec["gotcha"].prefix]

        args.extend(self.with_or_without("spath", activation_value="prefix"))
        args.extend(self.enable_or_disable("mpi-mount", variant="auto-mount"))
        args.extend(self.enable_or_disable("fortran"))
        args.extend(self.enable_or_disable("pmi"))
        args.extend(self.enable_or_disable("pmix"))
        args.extend(self.enable_or_disable("preload"))

        if self.debug_build:
            args.append("--disable-silent-rules")
        else:
            args.append("--enable-silent-rules")

        return args

    @when("@develop")
    def autoreconf(self, spec, prefix):
        sh = which("sh")
        sh("./autogen.sh")

    @when("%cce@11.0.3:")
    def patch(self):
        filter_file("-Werror", "", "client/src/Makefile.in")
        filter_file("-Werror", "", "client/src/Makefile.am")
