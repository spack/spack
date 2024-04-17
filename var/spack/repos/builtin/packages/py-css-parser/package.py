# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCssParser(PythonPackage):
    """A CSS Cascading Style Sheets library for Python."""

    homepage = "https://github.com/ebook-utils/css-parser"
    pypi = "css-parser/css-parser-1.0.9.tar.gz"

    maintainers("LydDeb")

    license("LGPL-3.0-or-later")

    version(
        "1.0.9",
        sha256="e18f66961103b61df25aa6df0dc808ab61c23e65ae6c1a8c149fe71911190495",
        url="https://pypi.org/packages/9e/42/3842eec3be1ab4278b263dd79f9190b610b72e9ff8b13680de09884be9b9/css_parser-1.0.9-py2.py3-none-any.whl",
    )
