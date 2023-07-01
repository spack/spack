# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqt5(SIPPackage):
    """PyQt is a set of Python v2 and v3 bindings for The Qt Company's Qt
    application framework and runs on all platforms supported by Qt including
    Windows, OS X, Linux, iOS and Android. PyQt5 supports Qt v5."""

    homepage = "https://www.riverbankcomputing.com/software/pyqt/intro"
    url = "https://files.pythonhosted.org/packages/source/P/PyQt5/PyQt5-5.15.9.tar.gz"
    list_url = "https://pypi.org/simple/PyQt5/"

    sip_module = "PyQt5.sip"

    version("5.15.9", sha256="dc41e8401a90dc3e2b692b411bd5492ab559ae27a27424eed4bd3915564ec4c0")
    version(
        "5.13.1",
        sha256="54b7f456341b89eeb3930e786837762ea67f235e886512496c4152ebe106d4af",
        deprecated=True,
    )
    version(
        "5.13.0",
        sha256="0cdbffe5135926527b61cc3692dd301cd0328dd87eeaf1313e610787c46faff9",
        deprecated=True,
    )
    version(
        "5.12.3",
        sha256="0db0fa37debab147450f9e052286f7a530404e2aaddc438e97a7dcdf56292110",
        deprecated=True,
    )

    # API files can be installed regardless if Qscintilla is installed or not
    variant("qsci_api", default=False, description="Install PyQt API file for QScintilla")

    # pyproject.toml
    depends_on("py-sip@6.6.2:6", type="build")
    depends_on("py-pyqt-builder@1.14.1:1", type="build")

    # PKG-INFO
    depends_on("py-pyqt5-sip@12.11:12", type=("build", "run"))

    # Without opengl support, I got the following error:
    # sip: QOpenGLFramebufferObject is undefined
    depends_on("qt@5+opengl")

    # https://www.riverbankcomputing.com/static/Docs/PyQt5/installation.html
    def configure_args(self):
        args = [
            "--pyuic5-interpreter",
            self.spec["python"].command.path,
            "--sipdir",
            self.prefix.share.sip.PyQt5,
            "--designer-plugindir",
            self.prefix.plugins.designer,
            "--qml-plugindir",
            self.prefix.plugins.PyQt5,
            "--stubsdir",
            join_path(python_platlib, "PyQt5"),
        ]
        if "+qsci_api" in self.spec:
            args.extend(["--qsci-api", "--qsci-api-destdir", self.prefix.share.qsci])
        return args

    def setup_run_environment(self, env):
        env.prepend_path("QT_PLUGIN_PATH", self.prefix.plugins)
