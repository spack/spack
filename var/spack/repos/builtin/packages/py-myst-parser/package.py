# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMystParser(PythonPackage):
    """A Sphinx and Docutils extension to parse MyST, a rich and
    extensible flavour of Markdown for authoring technical and
    scientific documentation."""

    homepage = "https://github.com/executablebooks/MyST-Parser"
    pypi = "myst-parser/myst-parser-0.18.1.tar.gz"

    license("MIT")

    version(
        "0.18.1",
        sha256="61b275b85d9f58aa327f370913ae1bec26ebad372cc99f3ab85c8ec3ee8d9fb8",
        url="https://pypi.org/packages/72/fd/594c936c65e707deda5670e8fff5ca2c948a12e922813eab5d316694e9ca/myst_parser-0.18.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.17:1")
        depends_on("py-docutils@0.15:0.19", when="@0.18.1:1")
        depends_on("py-jinja2")
        depends_on("py-markdown-it-py@1.0.0:2", when="@0.16:1")
        depends_on("py-mdit-py-plugins@0.3.1:0.3", when="@0.18.1:0.18")
        depends_on("py-pyyaml")
        depends_on("py-sphinx@4.0.0:5", when="@0.18")
        depends_on("py-typing-extensions", when="@0.17:0.18")
