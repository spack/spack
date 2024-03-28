# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLarkParser(PythonPackage):
    """Lark is a modern general-purpose parsing library for Python."""

    homepage = "https://github.com/lark-parser/lark/"
    pypi = "lark-parser/lark-parser-0.6.2.tar.gz"

    license("MIT")

    version(
        "0.12.0",
        sha256="0eaf30cb5ba787fe404d73a7d6e61df97b21d5a63ac26c5008c78a494373c675",
        url="https://pypi.org/packages/76/00/90f05db333fe1aa6b6ffea83a35425b7d53ea95c8bba0b1597f226cf1d5f/lark_parser-0.12.0-py2.py3-none-any.whl",
    )
