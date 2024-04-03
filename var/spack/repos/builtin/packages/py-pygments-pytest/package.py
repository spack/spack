# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygmentsPytest(PythonPackage):
    """A pygments lexer for pytest output."""

    homepage = "https://github.com/asottile/pygments-pytest"
    pypi = "pygments-pytest/pygments_pytest-1.2.0.tar.gz"

    license("MIT")

    version(
        "1.2.0",
        sha256="b40b23c32cfed8825b2551448b9327905343600f07ba0824ebf5be2b05c88d32",
        url="https://pypi.org/packages/6e/86/1704b81d451c1707acd8bd596a632f1bcc6fbe183c83dfc45a4b35ebc0b7/pygments_pytest-1.2.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pygments")
