# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.puk import Puk


class Pukabi(AutotoolsPackage):
    """PukABI: ABI manager for PadicoTM.

    PukABI is an ABI manager used by PadicoTM and NewMadeleine. It is
    able to intercept symbols of the libc, so as to install a virtual
    version or to add hooks.
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
    variant("mem", default=True, description="intercept memory-related symbols")
    variant("fsys", default=False, description="intercept filesystem-related symbols")
    variant("proc", default=False, description="intercept process-related symbols")
    variant("errno", default=False, description="intercept errno symbols")
    variant("sleep", default=False, description="intercept sleep symbols")
    variant("file", default=False, description="intercept FILE*-related symbols")
    variant("resolv", default=False, description="intercept DNS resolver-related symbols")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("autoconf@2.69:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("gmake", type="build")

    for v in Puk.versions:
        depends_on(f"puk@{v}", when=f"@{v}")

    conflicts("platform=darwin", msg="Darwin is not supported.")
    conflicts("platform=windows", msg="Windows is not supported.")
    conflicts("%gcc@:5", msg="Requires at least gcc 6.")
    conflicts("%gcc@14:", when="@:2024-07-12", msg="Older release do not support gcc >= 14")

    configure_directory = "PukABI"
    build_directory = "build"

    def autoreconf(self, spec, prefix):
        with working_dir(self.configure_directory):
            Executable("./autogen.sh")()

    def configure_args(self):
        config_args = []
        config_args += self.enable_or_disable("optimize")
        config_args += self.enable_or_disable("debug")
        config_args += self.enable_or_disable("fsys")
        config_args += self.enable_or_disable("proc")
        config_args += self.enable_or_disable("mem")
        config_args += self.enable_or_disable("errno")
        config_args += self.enable_or_disable("sleep")
        config_args += self.enable_or_disable("file")
        config_args += self.enable_or_disable("resolv")
        return config_args
