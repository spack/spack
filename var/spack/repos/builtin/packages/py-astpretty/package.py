# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAstpretty(PythonPackage):
    """Pretty print the output of python stdlib `ast.parse`."""

    homepage = "https://github.com/asottile/astpretty"
    pypi = "astpretty/astpretty-2.0.0.tar.gz"

    license("MIT")

    version(
        "2.0.0",
        sha256="7f27633ed885033da8b58666e7079ffff7e8e01869ec1aa66484cb5185ea3aa4",
        url="https://pypi.org/packages/34/8e/93b94d3c6dc00446ddf33d0e82490fcc52b094a0fd59bf5433158da330e5/astpretty-2.0.0-py2.py3-none-any.whl",
    )

    variant("typed", default=False, description="Add support for typed comments")

    with default_args(type=("build", "run")):
        depends_on("py-typed-ast", when="@1.4:2+typed")
