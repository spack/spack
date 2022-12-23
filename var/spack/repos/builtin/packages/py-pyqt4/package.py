# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqt4(SIPPackage):
    """PyQt is a set of Python v2 and v3 bindings for The Qt Company's Qt
    application framework and runs on all platforms supported by Qt including
    Windows, OS X, Linux, iOS and Android. PyQt4 supports Qt v4 and will build
    against Qt v5."""

    homepage = "https://www.riverbankcomputing.com/software/pyqt/intro"
    url = "https://www.riverbankcomputing.com/static/Downloads/PyQt4/4.12.3/PyQt4_gpl_x11-4.12.3.tar.gz"

    version("4.12.3", sha256="a00f5abef240a7b5852b7924fa5fdf5174569525dc076cd368a566619e56d472")
    version(
        "4.11.3",
        sha256="853780dcdbe2e6ba785d703d059b096e1fc49369d3e8d41a060be874b8745686",
        url="http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.3/PyQt-x11-gpl-4.11.3.tar.gz",
        deprecated=True,
    )

    # Requires distutils
    depends_on("python@:3.11", type=("build", "link", "run"))
    depends_on("qt@4")
    depends_on("py-sip@4.16.4:4.19.18 module=PyQt4.sip")

    build_directory = "."

    def configure_args(self):
        # https://www.riverbankcomputing.com/static/Docs/PyQt4/installation.html
        args = [
            "--verbose",
            "--confirm-license",
            "--qmake",
            self.spec["qt"].prefix.bin.qmake,
            "--sip",
            self.spec["py-sip"].prefix.bin.sip,
            "--sip-incdir",
            join_path(self.spec["py-sip"].prefix, self.spec["python"].package.include),
            "--bindir",
            self.prefix.bin,
            "--destdir",
            python_platlib,
            "--pyuic4-interpreter",
            self.spec["python"].command.path,
            "--sipdir",
            self.prefix.share.sip.PyQt4,
            "--stubsdir",
            join_path(python_platlib, "PyQt4"),
        ]
        return args

    def configure(self, spec, prefix):
        python("configure-ng.py", *self.configure_args())

    @run_after("install")
    def extend_path_setup(self):
        # https://github.com/spack/spack/issues/14121
        # https://github.com/spack/spack/pull/15297
        # Same code comes by default with py-pyqt5 and py-pyqt6
        text = """
# Support PyQt4 sub-packages that have been created by setuptools.
__path__ = __import__('pkgutil').extend_path(__path__, __name__)
"""
        with open(join_path(python_platlib, "PyQt4", "__init__.py"), "a") as f:
            f.write(text)
