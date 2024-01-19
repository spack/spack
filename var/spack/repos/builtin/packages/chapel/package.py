# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Chapel(AutotoolsPackage):
    """Chapel is a modern programming language that is parallel, productive,
    portable, scalable and open-source."""

    homepage = "https://chapel-lang.org/"

    url = "https://github.com/chapel-lang/chapel/archive/refs/tags/1.33.0.tar.gz"
    git = "https://github.com/chapel-lang/chapel.git"

    # A list of GitHub accounts to notify when the package is updated.
    maintainers("arezaii")

    # See https://spdx.org/licenses/ for a list.
    license("Apache-2.0")

    version("main", branch="main")

    version("1.33.0", sha256="c7dfe691a043b6a5dcbea6fe7607ca030014f1a8019744c4c99f67caa8829ba3")
    version("1.32.0", sha256="a359032b4355774e250fb2796887b3bbf58d010c468faba97f7b471bc6bab57d")
    version("1.31.0", sha256="bf9a63f7e5d1f247e8680c9a07aeb330cbbf199777a282408100a87dda95918f")
    version("1.30.0", sha256="d7d82f64f405b8c03e2ce6353d16aba5a261d3f0c63dc3bb64ea3841cfa597b9")
    version(
        "1.29.0",
        deprecated=True,
        sha256="7fcd13db8e27f14d586358d4c2587e43c8f21d408126fa0ca27d1b7067b867c0",
    )
    version(
        "1.28.0",
        deprecated=True,
        sha256="321243a91f8f2dfb3b37a714e2d45298e6a967a9a115565f9ad9cc630ff0bd0e",
    )
    # Do NOT add older versions here.
    # Chapel releases over 2 years old are not supported.

    depends_on("doxygen@1.8.17:")

    variant(
        "llvm",
        default="unset",
        description="LLVM backend type. Use value 'spack' to have spack "
        "handle the LLVM package",
        values=("none", "system", "bundled", "spack", "unset"),
    )

    variant(
        "comm",
        default="none",
        description="Build Chapel with multi-locale support",
        values=("none", "gasnet", "ofi"),
    )
    variant(
        "substrate",
        default="none",
        description="Build Chapel with mulit-locale support using the "
        "supplied CHPL_COMM_SUBSTRATE",
        values=("none", "udp", "ibv", "ofi"),
        multi=False,
    )

    package_module_opts = ("zmq", "libevent", "protobuf", "ssl", "hdf5", "yaml")
    package_module_dict = {
        "zmq": "libzmq",
        "libevent": "libevent",
        "protobuf": "protobuf",
        "ssl": "openssl",
        "hdf5": "hdf5+hl~mpi",
        "yaml": "libyaml",
    }
    variant(
        "package_modules",
        description="Include package module dependencies with spack",
        values=disjoint_sets(("none",), ("all",), package_module_opts)
        .with_error("'none' or 'all' cannot be activated along with other package_modules")
        .with_default("none")
        .with_non_feature_values("none", "all"),
    )

    for opt, dep in package_module_dict.items():
        depends_on(dep, when="package_modules={0}".format(opt), type="run")
        depends_on(dep, when="package_modules=all", type="run")

    platform_opts = (
        "unset",
        "cygwin32",
        "cygwin64",
        "darwin",
        "linux32",
        "linux64",
        "netbsd32",
        "netbsd64",
        "pwr6",
        "cray-cs",
        "cray-xc",
        "hpe-apollo",
        "hpe-cray-ex",
    )

    variant(
        "host_platform",
        description="Host platform",
        default="unset",
        values=platform_opts,
        multi=False,
    )

    variant(
        "target_platform",
        description="Target platform for cross compilation",
        default="unset",
        values=platform_opts,
        multi=False,
    )

    variant(
        "tasks",
        description="Select tasking layer for intra-locale parallelism",
        default="qthreads",
        values=("qthreads", "fifo"),
        multi=False,
    )

    variant(
        "re2",
        description="Build with re2 support",
        default="bundled",
        values=("none", "bundled"),
        multi=False,
    )

    variant(
        "gmp",
        description="Build with gmp support",
        default="unset",
        values=("unset", "system", "none", "bundled"),
        multi=False,
    )

    variant(
        "hwloc",
        description="Build with hwloc support",
        default="bundled",
        values=("none", "bundled"),
        multi=False,
    )

    variant(
        "aux_filesys",
        description="Build with runtime support for certain filesystems",
        default="none",
        values=("none", "lustre"),
        multi=False,
    )

    variant(
        "locale_model",
        values=("flat", "numa"),
        default="flat",
        description="Locale model to use",
        multi=False,
    )

    variant(
        "mem",
        values=("cstdlib", "jemalloc"),
        default="jemalloc",
        description="Memory management layer",
        multi=False,
    )

    variant(
        "host_mem",
        values=("cstdlib", "jemalloc"),
        default="jemalloc",
        description="Memory management layer for the chpl compiler",
        multi=False,
    )

    variant(
        "host_jemalloc",
        values=("none", "bundled", "system"),
        multi=False,
        description="Selects between no jemalloc, bundled jemalloc, or system jemalloc",
    )

    variant(
        "lib_pic",
        values=("pic", "none"),
        default="none",
        description="Build position-independent code suitable for shared libraries",
    )

    chpl_env_vars = [
        "CHPL_HOME",
        "CHPL_HOST_PLATFORM",
        "CHPL_HOST_COMPILER",
        "CHPL_HOST_CC",
        "CHPL_HOST_CXX",
        "CHPL_HOST_ARCH",
        "CHPL_TARGET_PLATFORM",
        "CHPL_TARGET_COMPILER",
        "CHPL_TARGET_CC",
        "CHPL_TARGET_CXX",
        "CHPL_TARGET_LD",
        "CHPL_TARGET_ARCH",
        "CHPL_TARGET_CPU",
        "CHPL_LOCALE_MODEL",
        "CHPL_COMM",
        "CHPL_TASKS",
        "CHPL_LAUNCHER",
        "CHPL_TIMERS",
        "CHPL_UNWIND",
        "CHPL_HOST_MEM",
        "CHPL_MEM",
        "CHPL_ATOMICS",
        "CHPL_GMP",
        "CHPL_HWLOC",
        "CHPL_RE2",
        "CHPL_LLVM",
        "CHPL_LLVM_SUPPORT",
        "CHPL_LLVM_CONFIG",
        "CHPL_LLVM_VERSION",
        "CHPL_AUX_FILESYS",
        "CHPL_LIB_PIC",
        "CHPL_SANITIZE",
        "CHPL_SANITIZE_EXE",
    ]

    # Add dependencies
    depends_on("llvm@14:16", when="llvm=spack")
    depends_on("m4")

    # TODO: Spack needs both of these, so do we even need to specify them?
    depends_on("python@3.7:3.10")
    depends_on("cmake@3.16:")

    def unset_chpl_env_vars(self, env):
        for var in self.chpl_env_vars:
            env.unset(var)

    def configure(self, spec, prefix):
        configure("--prefix={0}".format(prefix))

    def setup_chpl_comm(self, env, spec):
        env.set("CHPL_COMM", spec.variants["comm"].value)
        if spec.variants["substrate"].value != "none":
            env.set("CHPL_COMM_SUBSTRATE", spec.variants["substrate"].value)

    def setup_chpl_llvm(self, env, spec):
        # Setup LLVM environment variables based on spec
        if spec.variants["llvm"].value == "spack":
            env.set("CHPL_LLVM_CONFIG", "{0}/{1}".format(spec["llvm"].prefix, "/bin/llvm-config"))
            env.set("CHPL_LLVM", "system")
        elif spec.variants["llvm"].value != "unset":
            env.set("CHPL_LLVM", spec.variants["llvm"].value)

    def setup_env_vars(self, env):
        self.setup_chpl_llvm(env, self.spec)
        env.set("CHPL_AUX_FILESYSTEM", self.spec.variants["aux_filesys"].value)
        env.set("CHPL_DEVELOPER", "0")  # TODO: handle this better, maybe with a variant
        env.set("CHPL_RE2", self.spec.variants["re2"].value)
        env.set("CHPL_HWLOC", self.spec.variants["hwloc"].value)
        if self.spec.variants["host_platform"].value != "unset":
            env.set("CHPL_HOST_PLATFORM", self.spec.variants["host_platform"].value)
        if self.spec.variants["target_platform"].value != "unset":
            env.set("CHPL_TARGET_PLATFORM", self.spec.variants["target_platform"].value)
        if self.spec.variants["gmp"].value != "unset":
            env.set("CHPL_GMP", self.spec.variants["gmp"].value)

        self.setup_chpl_comm(env, self.spec)

    def setup_build_environment(self, env):
        self.unset_chpl_env_vars(env)
        self.setup_env_vars(env)

    def setup_run_environment(self, env):
        self.setup_env_vars(env)
