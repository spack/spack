# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLatexcodec(PythonPackage):
    """A lexer and codec to work with LaTeX code in Python."""

    homepage = "https://latexcodec.readthedocs.io"
    pypi = "latexcodec/latexcodec-1.0.4.tar.gz"

    license("MIT")

    version(
        "1.0.4",
        sha256="f896e28da6ebb38674206558b5fec10192c3db1620aa7c570a314057bd3477e8",
        url="https://pypi.org/packages/8b/fb/aebbbcf55fed706d520d17e2573a9a393606dd8df886fca97e3a8e6b47b9/latexcodec-1.0.4-py2.py3-none-any.whl",
    )
