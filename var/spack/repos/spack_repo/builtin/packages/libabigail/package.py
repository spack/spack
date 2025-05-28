# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Libabigail(AutotoolsPackage):
    """The ABI Generic Analysis and Instrumentation Library"""

    homepage = "https://sourceware.org/libabigail"
    git = "https://sourceware.org/git/libabigail.git"

    license("Apache-2.0 WITH LLVM-exception")

    version("master", branch="master")
    version("2.7", sha256="467c5b91b655fe82c54f92b35a7c2155e0dd9f5f052a4e4e21caf245e092c2ca")
    version("2.6", sha256="3bfa8ba753ff27722baa7f73b15a475f8a4599355e47439108423d1912bb5469")
    version("2.5", sha256="7cfc4e9b00ae38d87fb0c63beabb32b9cbf9ce410e52ceeb5ad5b3c5beb111f3")
    version("2.4", sha256="5fe76b6344188a95f693b84e1b8731443d274a4c4b0ebee18fc00d9aedac8509")
    version("2.3", sha256="bc214c89f3b7ab8f20113a7c7aa40a207d41574d7ec25c2520501420d8019eb0")
    version("2.2", sha256="764d3d811550fadcca1e86e48a09564d0037a5210f54b24780becfa59095116b")
    version("2.1", sha256="4a6297d41d15d1936256117116bd61296e6b9bee23d54a0caf8d3f5ab8ddcc4c")
    version("2.0", sha256="3704ae97a56bf076ca08fb5dea6b21db998fbbf14c4f9de12824b78db53b6fda")
    version("1.8", sha256="1cbf260b894ccafc61b2673ba30c020c3f67dbba9dfa88dca3935dff661d665c")

    variant("docs", default=False, description="build documentation")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("elfutils", type=("build", "link"))
    depends_on("libxml2", type=("build", "link"))
    depends_on("xxhash", type=("build", "link"), when="@2.2:")

    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")

    # Libabigail won't generate it's bin without Python
    depends_on("python@3.8:")

    # Will not find libxml without this
    depends_on("pkgconfig", type="build")

    # Documentation dependencies
    depends_on("doxygen", type="build", when="+docs")
    depends_on("py-sphinx", type="build", when="+docs")

    def url_for_version(self, version):
        ext = "xz" if version >= Version("2.2") else "gz"
        base = "https://mirrors.kernel.org/sourceware/libabigail"
        url = f"{base}/libabigail-{version.dotted}.tar.{ext}"
        return url

    def configure_args(self):
        spec = self.spec
        config_args = [f"CPPFLAGS=-I{spec['libxml2'].prefix}/include"]
        config_args.append(
            "LDFLAGS=-L{0} -Wl,-rpath,{0}".format(spec["libxml2"].libs.directories[0])
        )
        return config_args

    def autoreconf(self, spec, prefix):
        autoreconf = which("autoreconf")
        with working_dir(self.configure_directory):
            # We need force (f) because without it, looks for RedHat library
            autoreconf("-ivf")
