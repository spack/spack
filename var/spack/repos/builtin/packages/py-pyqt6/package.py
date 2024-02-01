# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqt6(SIPPackage):
    """PyQt6 is a comprehensive set of Python bindings for Qt v6."""

    homepage = "https://www.riverbankcomputing.com/software/pyqt/"
    url = "https://files.pythonhosted.org/packages/source/P/PyQt6/PyQt6-6.5.1.tar.gz"
    list_url = "https://pypi.org/simple/PyQt6/"

    license("GPL-3.0-or-later")

    version("6.5.2", sha256="1487ee7350f9ffb66d60ab4176519252c2b371762cbe8f8340fd951f63801280")
    version("6.5.1", sha256="e166a0568c27bcc8db00271a5043936226690b6a4a74ce0a5caeb408040a97c3")

    # pyproject.toml
    depends_on("py-sip@6.5:6", type="build")
    depends_on("py-pyqt-builder@1.15:1", type="build")

    # PKG-INFO
    depends_on("py-pyqt6-sip@13.4:13", type=("build", "run"))

    # README
    depends_on("qt-base@6")

    def setup_build_environment(self, env):
        # Detected system locale encoding (US-ASCII, locale "C") is not UTF-8.
        # Qt shall use a UTF-8 locale ("UTF-8") instead. If this causes problems,
        # reconfigure your locale. See the locale(1) manual for more information.
        env.set("LC_ALL", "en_US.UTF-8")

    def configure_args(self):
        # https://www.riverbankcomputing.com/static/Docs/PyQt6/installation.html
        return ["--confirm-license", "--no-make", "--qmake", self.spec["qt-base"].prefix.bin.qmake]
