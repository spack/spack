# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMistletoe(PythonPackage):
    """A fast, extensible Markdown parser in pure Python."""

    homepage = "https://github.com/miyuchina/mistletoe"
    pypi = "mistletoe/mistletoe-1.2.1.tar.gz"

    license("MIT")

    version(
        "1.2.1",
        sha256="620563ac06380ce0629b4a2afa2f2ab797ffac3efdcccaf2362a7266600e6dcc",
        url="https://pypi.org/packages/2a/98/399f57478bd84f5bc568f92b630a0e6b7bd9b7d0e7a86e98614a5abab8bc/mistletoe-1.2.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3")
