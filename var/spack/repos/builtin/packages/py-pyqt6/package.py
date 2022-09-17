# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqt6(PythonPackage):
    """PyQt6 is a comprehensive set of Python bindings for Qt v6."""

    homepage = "https://www.riverbankcomputing.com/software/pyqt/"
    pypi = "PyQt6/PyQt6-6.3.1.tar.gz"

    version("6.3.1", sha256="8cc6e21dbaf7047d1fc897e396ccd9710a12f2ef976563dad65f06017d2c9757")

    depends_on("python@3.6.1:", type=("build", "run"))
    depends_on("py-sip@6.5:6", type="build")
    depends_on("py-pyqt-builder@1.11:1", type="build")
    depends_on("qt@6")
