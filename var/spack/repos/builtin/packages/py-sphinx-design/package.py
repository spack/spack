# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxDesign(PythonPackage):
    """A sphinx extension for designing beautiful, screen-size responsive web components."""

    homepage = "https://sphinx-design.readthedocs.io"
    pypi = "sphinx-design/sphinx_design-0.3.0.tar.gz"

    maintainers("ax3l", "adamjstewart")

    license("MIT")

    version(
        "0.4.1",
        sha256="23bf5705eb31296d4451f68b0222a698a8a84396ffe8378dfd9319ba7ab8efd9",
        url="https://pypi.org/packages/c2/8a/7538087272110d010cd27024c392dca176315ad7dfc3f3df3f99798cc21b/sphinx_design-0.4.1-py3-none-any.whl",
    )
    version(
        "0.4.0",
        sha256="49ca06a29700e6e4e33ed7b0da0919d1993cd570ac5f0a64b56a904ad6c6f1ad",
        url="https://pypi.org/packages/f2/43/262805888ac91b83f485e57ffae94606d078cd534daf3dee5a33e6111dcd/sphinx_design-0.4.0-py3-none-any.whl",
    )
    version(
        "0.3.0",
        sha256="823c1dd74f31efb3285ec2f1254caefed29d762a40cd676f58413a1e4ed5cc96",
        url="https://pypi.org/packages/89/aa/9872f086a8f483f86f174d3eb03c6954b01e851e151c4ddbd5bf758a9402/sphinx_design-0.3.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.1:0.4")
        depends_on("py-sphinx@4.0.0:6", when="@0.4")
        depends_on("py-sphinx@4.0.0:5", when="@0.2:0.3")
