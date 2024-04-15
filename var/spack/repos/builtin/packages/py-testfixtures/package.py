# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTestfixtures(PythonPackage):
    """Testfixtures is a collection of helpers and mock objects that are useful
    when writing automated tests in Python."""

    homepage = "https://github.com/Simplistix/testfixtures"
    url = "https://github.com/Simplistix/testfixtures/archive/6.16.0.zip"

    license("MIT")

    version(
        "6.16.0",
        sha256="017f1924f464189915e67162f530758537175ddd1461b211c666f0587ebc2939",
        url="https://pypi.org/packages/2b/93/8e1da41ef50d4e13f3a16c586dd366556bf2c6840defc4b87ed9ab10b923/testfixtures-6.16.0-py2.py3-none-any.whl",
    )
