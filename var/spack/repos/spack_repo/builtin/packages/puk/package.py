# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Puk(AutotoolsPackage):
    """Puk: Padico micro-kernel.

    Puk is the foundation module of PadicoTM. Its task is to manage
    modules (loading, running and unloading). It comes with a powerful
    component model used to assemble a communication stack.
    """

    homepage = "https://pm2.gitlabpages.inria.fr/"
    url = "https://pm2.gitlabpages.inria.fr/releases/pm2-2025-03-18.tar.gz"
    list_url = "https://pm2.gitlabpages.inria.fr/releases/"
    git = "https://gitlab.inria.fr/pm2/pm2.git"

    maintainers("a-denis")
    license("GPL-2.0-or-later", checked_by="a-denis")

    def url_for_version(self, version):
        url = "https://pm2.gitlabpages.inria.fr/releases/pm2-{0}.tar.gz"
        return url.format(version)

    version("master", branch="master")
    version(
        "2025-03-18", sha256="2d0208809dd17bac4fd7e7f97b22e2240b925d8828b9ab5dc5f435e58ff97010"
    )
    version(
        "2024-11-21", sha256="76da169bbb9720a13be1f750480e1a7d6510830163878852876932639879d632"
    )
    version(
        "2024-07-12", sha256="ea9bb91b213950a52eb99d787110905d45ed02954ea9133596d690db5be0c31b"
    )
    version(
        "2022-05-31", sha256="afd19809a5a520a477ab596f951bbde3209868ab16febbc246592e8aed20c3ca"
    )
    version(
        "2021-05-21", sha256="6a207b032e623b8be0196a42dcaf4311bfe45ede2e044bd47611b6610c04c61e"
    )

    variant("optimize", default=True, description="Build in optimized mode")
    variant("debug", default=False, description="Build in debug mode")
    variant("trace", default=False, description="enable Puk traces")
    variant("profile", default=False, description="enable Puk memory profiling")
    variant("asan", default=False, description="Build with Address Sanitizer (ASAN)")
    variant("builtin", default=False, description="Build all modules as builtin")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("autoconf@2.69:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("gmake", type="build")

    depends_on("bash")
    depends_on("expat@2.1.0:")
    depends_on("gdb", when="+debug", type=("build", "run"))
    depends_on("valgrind", when="+debug", type=("build", "run"))

    conflicts("platform=darwin", msg="Darwin is not supported.")
    conflicts("platform=windows", msg="Windows is not supported.")
    conflicts("%gcc@:5", msg="Requires at least gcc 6.")
    conflicts("%gcc@14:", when="@:2024-07-12", msg="Older release do not support gcc >= 14")

    configure_directory = "Puk"
    build_directory = "build"

    def autoreconf(self, spec, prefix):
        with working_dir(self.configure_directory):
            Executable("./autogen.sh")()

    def configure_args(self):
        config_args = [
            "--enable-lfqueue=nblfq",  # use nblfq by default for production
            "--without-simgrid",  # no simgrid support with spack for now
        ]
        config_args += self.enable_or_disable("optimize")
        config_args += self.enable_or_disable("debug")
        config_args += self.enable_or_disable("asan")
        config_args += self.enable_or_disable("trace")
        config_args += self.enable_or_disable("profile")
        config_args += self.enable_or_disable("builtin")
        return config_args
