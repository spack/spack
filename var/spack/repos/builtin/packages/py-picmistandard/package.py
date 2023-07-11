# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPicmistandard(PythonPackage):
    """Standard input format for Particle-In-Cell codes"""

    homepage = "https://picmi-standard.github.io"
    git = "https://github.com/picmi-standard/picmi.git"
    pypi = "picmistandard/picmistandard-0.0.18.tar.gz"

    maintainers("ax3l", "dpgrote", "RemiLehe")

    version("develop", branch="master")
    version("0.25.0", sha256="0a78b3b17054d0861626287ace1fb9321469a9c95795b92981103b27d7797f67")
    version("0.24.0", sha256="55a82adcc14b41eb612caf0d9e47b0e2a56ffc196a58b41fa0cc395c6924be9a")
    version("0.23.2", sha256="e6b4c46b23520d0a97b904df90d53ff6a3209b2b6b2fa741f684c594429a591c")
    version("0.23.1", sha256="90ad1d3d2759d910cfdb88484516b7d0434ec98e881af46961b7e2faa534434d")
    version("0.0.22", sha256="e234a431274254b22cd70be64d6555b383d98426b2763ea0c174cf77bf4d0890")
    version("0.0.21", sha256="930056a23ed92dac7930198f115b6248606b57403bffebce3d84579657c8d10b")
    version("0.0.20", sha256="9c1822eaa2e4dd543b5afcfa97940516267dda3890695a6cf9c29565a41e2905")
    version("0.0.19", sha256="4b7ba1330964fbfd515e8ea2219966957c1386e0896b92d36bd9e134afb02f5a")
    version("0.0.18", sha256="68c208c0c54b4786e133bb13eef0dd4824998da4906285987ddee84e6d195e71")
    # 0.15 - 0.17 have broken install logic: missing requirements.txt on pypi
    version(
        "0.0.16",
        sha256="b7eefdae1c43119984226b2df358c86fdeef7495084e47b3575e3d07e790ba30",
        url="https://github.com/picmi-standard/picmi/archive/refs/tags/0.0.14.tar.gz",
    )
    version("0.0.14", sha256="8f83b25b281fc0309a0c4f75c7605afd5fa0ef4df3b3ac115069478c119bc8c3")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-numpy@1.15:1", type=("build", "run"))
    depends_on("py-scipy@1.5:1", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    @property
    def build_directory(self):
        if self.spec.satisfies("@develop") or self.spec.satisfies("@0.0.16"):
            return "PICMI_Python"
        else:
            return "./"
