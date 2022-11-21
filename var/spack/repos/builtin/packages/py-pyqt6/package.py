# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqt6(SIPPackage):
    """PyQt6 is a comprehensive set of Python bindings for Qt v6."""

    homepage = "https://www.riverbankcomputing.com/software/pyqt/"
    url = "https://files.pythonhosted.org/packages/source/P/PyQt6/PyQt6-6.4.0.tar.gz"
    list_url = "https://pypi.org/simple/PyQt6/"

    version("6.4.0", sha256="91392469be1f491905fa9e78fa4e4059a89ab616ddf2ecfd525bc1d65c26bb93")

    depends_on("python@3.6.1:", type=("build", "run"))
    depends_on("py-sip@6.5:6", type="build")
    depends_on("py-pyqt-builder@1.11:1", type="build")
    depends_on("qt-base@6")

    def configure_args(self):
        # https://www.riverbankcomputing.com/static/Docs/PyQt6/installation.html
        return ["--confirm-license", "--no-make", "--qmake", self.spec["qt-base"].prefix.bin.qmake]
