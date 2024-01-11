# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

### Taken from upcxx/package.py to detect Cray systems
def is_CrayXC():
    return (spack.platforms.host().name in ["linux", "cray"]) and (
        os.environ.get("CRAYPE_NETWORK_TARGET") == "aries"
    )


def is_CrayEX():
    if spack.platforms.host().name in ["linux", "cray"]:
        target = os.environ.get("CRAYPE_NETWORK_TARGET")
        if target in ["ofi", "ucx"]:  # normal case
            return True
        elif target is None:  # but some systems lack Cray PrgEnv
            fi_info = which("fi_info")
            if fi_info and fi_info("-l", output=str).find("cxi") >= 0:
                return True
    return False


def cross_detect():
    if is_CrayXC():
        if which("srun"):
            return "cray-aries-slurm"
        if which("aprun"):
            return "cray-aries-alps"
    return "none"
###

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
    version("1.29.0",
            deprecated=True,
            sha256="7fcd13db8e27f14d586358d4c2587e43c8f21d408126fa0ca27d1b7067b867c0")
    version("1.28.0",
            deprecated=True,
            sha256="321243a91f8f2dfb3b37a714e2d45298e6a967a9a115565f9ad9cc630ff0bd0e")
    # Do NOT add older versions here.
    # Chapel releases over 2 years old are not supported.

    depends_on("doxygen@1.8.17:")

    variant(
            "llvm", default="none",
            description="LLVM backend type. Use value 'spack' to have spack handle the LLVM package",
            values=("none", "system", "bundled", "spack")
    )

    variant(
            "comm",
            default="none",
            description="Build Chapel with multi-locale support",
            values=("none","gasnet","ofi")
    )
    variant(
            "substrate",
            default="none",
            description="Build Chapel with mulit-locale support using the supplied CHPL_COMM_SUBSTRATE",
            values=("none","udp","ibv","ofi"),
            multi=False
    )

    package_module_opts = ("zmq", "libevent", "protobuf", "ssl", "hdf5", "yaml")
    package_module_dict = {
                           "zmq":"libzmq",
                           "libevent":"libevent",
                           "protobuf":"protobuf",
                           "ssl":"openssl",
                           "hdf5":"hdf5+hl~mpi",
                           "yaml":"libyaml"
    }
    variant(
            "package_modules",
            description="Include package module dependencies with spack",
            values=disjoint_sets(
            ("none",),
            ("all",),
            package_module_opts,
        ).prohibit_empty_set().with_error(
            "'none' or 'all' cannot be activated along with other package_modules"
        ).with_default("none").with_non_feature_values("none", "all")
    )

    for opt, dep in package_module_dict.items():
        depends_on(dep, when="package_modules={0}".format(opt), type="run")
        depends_on(dep, when="package_modules=all", type="run")


    # Add dependencies
    depends_on("llvm@14:16", when="llvm=spack")
    depends_on("m4")

    # TODO: Spack needs both of these, so do we even need to specify them?
    depends_on("python@3.7:3.10")
    depends_on("cmake@3.16:")



    def setup_chpl_comm(self, env, spec):
        env.set("CHPL_COMM",spec.variants["comm"].value)
        if spec.variants["substrate"].value != "none":
            env.set("CHPL_COMM_SUBSTRATE",spec.variants["substrate"].value)

    def setup_build_environment(self, env):
        env.set("CHPL_LLVM", self.spec.variants["llvm"].value)
        env.set("CHPL_DEVELOPER","0")
        if self.spec.variants["llvm"].value=="spack":
            env.set("CHPL_LLVM_CONFIG",
                    "{0}/{1}".format(self.spec["llvm"].prefix, "/bin/llvm-config"))
            env.set("CHPL_LLVM", "system")
        self.setup_chpl_comm(env, self.spec)

    def setup_run_environment(self, env):
        self.setup_build_environment(env)
