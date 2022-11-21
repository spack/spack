# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqt5(SIPPackage):
    """PyQt is a set of Python v2 and v3 bindings for The Qt Company's Qt
    application framework and runs on all platforms supported by Qt including
    Windows, OS X, Linux, iOS and Android. PyQt5 supports Qt v5."""

    homepage = "https://www.riverbankcomputing.com/software/pyqt/intro"
    url = "https://files.pythonhosted.org/packages/source/P/PyQt5/PyQt5-5.15.7.tar.gz"
    list_url = "https://pypi.org/simple/PyQt5/"

    version("5.15.7", sha256="755121a52b3a08cb07275c10ebb96576d36e320e572591db16cfdbc558101594")
    version("5.13.1", sha256="54b7f456341b89eeb3930e786837762ea67f235e886512496c4152ebe106d4af", deprecated=True)
    version("5.13.0", sha256="0cdbffe5135926527b61cc3692dd301cd0328dd87eeaf1313e610787c46faff9", deprecated=True)
    version("5.12.3", sha256="0db0fa37debab147450f9e052286f7a530404e2aaddc438e97a7dcdf56292110", deprecated=True)

    depends_on("py-sip@6.4:6", type="build")
    depends_on("py-pyqt-builder@1.9:1", type="build")
    depends_on("qt@5")

    def configure_args(self):
        # https://www.riverbankcomputing.com/static/Docs/PyQt5/installation.html
        return ["--confirm-license", "--no-make", "--qmake", self.spec["qt"].prefix.bin.qmake]
