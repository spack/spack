# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyRequestsUnixsocket(PythonPackage):
    """Use requests to talk HTTP via a UNIX domain socket."""

    homepage = "https://github.com/msabramo/requests-unixsocket"
    pypi = "requests-unixsocket/requests-unixsocket-0.2.0.tar.gz"

    license("Apache-2.0")

    version("0.4.1", sha256="b2596158c356ecee68d27ba469a52211230ac6fb0cde8b66afb19f0ed47a1995")
    version("0.3.0", sha256="28304283ea9357d45fff58ad5b11e47708cfbf5806817aa59b2a363228ee971e")
    version("0.2.0", sha256="9e5c1a20afc3cf786197ae59c79bcdb0e7565f218f27df5f891307ee8817c1ea")

    depends_on("py-setuptools", when="@:0.3.0", type="build")
    depends_on("py-setuptools@64:", when="@0.4:", type="build")
    depends_on("py-setuptools-scm@8:", when="@0.4:", type="build")
    depends_on("python@3.9:", when="@0.4:", type=("build", "run"))
    depends_on("py-requests@1.1:", type=("build", "run"))
    depends_on("py-urllib3@1.8:", when="@:0.2.0", type=("build", "run"))

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/r/requests-unixsocket/requests{}unixsocket-{}.tar.gz"
        if version >= Version("0.3.1"):
            sep = "_"
        else:
            sep = "-"
        return url.format(sep, version)
