# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPox(PythonPackage):
    """Utilities for filesystem exploration and automated builds."""

    homepage = "https://github.com/uqfoundation/pox"
    pypi = "pox/pox-0.2.5.tar.gz"

    license("BSD-3-Clause")

    version("0.3.5", sha256="8120ee4c94e950e6e0483e050a4f0e56076e590ba0a9add19524c254bd23c2d1")
    version("0.3.4", sha256="16e6eca84f1bec3828210b06b052adf04cf2ab20c22fd6fbef5f78320c9a6fed")
    version("0.3.3", sha256="e1ced66f2a0c92a58cf3646bc7ccb8b4773d40884b76f85eeda0670474871667")
    version("0.3.2", sha256="e825225297638d6e3d49415f8cfb65407a5d15e56f2fb7fe9d9b9e3050c65ee1")
    version("0.3.1", sha256="cbb0c0acd650c0ffb620999da611e93aae5105c46a084c4ceaf2f704ed708c1e")
    version("0.3.0", sha256="cb968350b186466bb4905a21084587ec3aa6fd7aa0ef55d416ee0d523e2abe31")
    version("0.2.5", sha256="2b53fbdf02596240483dc2cb94f94cc21252ad1b1858c7b1c151afeec9022cc8")
    version("0.2.3", sha256="d3e8167a1ebe08ae56262a0b9359118d90bc4648cd284b5d10ae240343100a75")
    version("0.2.2", sha256="c0b88e59ef0e4f2fa4839e11bf90d2c32d6ceb5abaf01f0c8138f7558e6f87c1")
    version("0.2.1", sha256="580bf731fee233c58eac0974011b5bf0698efb7337b0a1696d289043b4fcd7f4")

    depends_on("python@2.5:2.8,3.1:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.6:", when="@0.3.0:", type=("build", "run"))

    depends_on("py-setuptools@0.6:", type="build")

    def url_for_version(self, version):
        url = "https://pypi.io/packages/source/p/pox/"
        if Version("0.3.0") > version >= Version("0.2.4"):
            url += "pox-{0}.tar.gz"
        else:
            url += "pox-{0}.zip"

        url = url.format(version)
        return url
