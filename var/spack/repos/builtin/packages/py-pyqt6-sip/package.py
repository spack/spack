# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqt6Sip(PythonPackage):
    """The sip module support for PyQt6."""

    homepage = "https://www.riverbankcomputing.com/software/sip/"
    pypi = "PyQt6-sip/PyQt6_sip-13.5.1.tar.gz"

    license("GPL-2.0-or-later")

    version("13.5.1", sha256="d1e9141752966669576d04b37ba0b122abbc41cc9c35493751028d7d91c4dd49")

    depends_on("py-setuptools@30.3:", type="build")
