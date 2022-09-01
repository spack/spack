# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMystParser(PythonPackage):
    """A Sphinx and Docutils extension to parse MyST, a rich and
    extensible flavour of Markdown for authoring technical and
    scientific documentation.
    """

    homepage = "https://github.com/executablebooks/MyST-Parser"

    documentation = "https://myst-parser.readthedocs.io/en/latest/"

    keywords = [
        "markdown",
        "lexer",
        "parser",
        "development",
        "docutils",
        "sphinx",
    ]

    pypi = "myst-parser/myst-parser-0.18.0.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]

    version("0.18.0", sha256="739a4d96773a8e55a2cacd3941ce46a446ee23dcd6b37e06f73f551ad7821d86")

    depends_on("python@3.7:", type=("build", "run"))

    depends_on("py-flit-core@3.4:3.99", type="build")

    depends_on("py-docutils@0.15:0.18.99", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-markdown-it-py@1.0.0:2.9.9", type=("build", "run"))
    depends_on("py-mdit-py-plugins@0.3:0.99", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-sphinx@4:5.99", type=("build", "run"))
