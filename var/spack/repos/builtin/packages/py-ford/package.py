# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFord(PythonPackage):
    """FORD, standing for FORtran Documenter, is an automatic documentation generator
    for modern Fortran programs."""

    pypi = "FORD/FORD-6.1.11.tar.gz"

    maintainers("wscullin")

    license("GPL-3.0-only")

    version(
        "6.1.13",
        sha256="701ecd4b8744714a50cd31a8b49a95a85d647716b9d971a60ab1b58c53032048",
        url="https://pypi.org/packages/b3/49/00fb42b10bcb6b241f3c29248afa55000554aa05fb67588a4f2616361953/FORD-6.1.13-py3-none-any.whl",
    )
    version(
        "6.1.12",
        sha256="ec520566fbc3738a1e471538a8db08637792be578b702f874180733b72378a53",
        url="https://pypi.org/packages/ea/14/27b4d5c21e182ad4107e570b9735cb702dced4b00d12c7e84704bba21b5c/FORD-6.1.12-py3-none-any.whl",
    )
    version(
        "6.1.11",
        sha256="313d5252e91430577e8038f62efa154daa0ed888ed8772fa96271f3209fd7c29",
        url="https://pypi.org/packages/80/b9/6666fe741098cce12c97c7b3faabb21a0f77f0b56d3237a0bdd94f34b90e/FORD-6.1.11-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-beautifulsoup4@4.5.1:")
        depends_on("py-graphviz", when="@:6.1.13,6.15:6")
        depends_on("py-importlib-metadata", when="@:6.1,6.15:6 ^python@:3.7")
        depends_on("py-jinja2@2.1:", when="@:6")
        depends_on("py-markdown", when="@:6.1.13,6.15:6")
        depends_on("py-markdown-include@0.5.1:", when="@:6.1.13,6.15:6")
        depends_on("py-pygments", when="@:6.1.13,6.15:6")
        depends_on("py-python-markdown-math@0.8:", when="@6.1.9:6.2,7:")
        depends_on("py-toposort", when="@:6.1.13,6.15:6")
        depends_on("py-tqdm", when="@:6.1.13,6.15:6")
