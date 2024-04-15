# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRst2pdf(PythonPackage):
    """Convert reStructured Text to PDF via ReportLab.

    The usual way of creating PDF from reStructuredText is by going through
    LaTeX. This tool provides an alternative by producing PDF directly using
    the ReportLab library."""

    homepage = "https://rst2pdf.org/"
    pypi = "rst2pdf/rst2pdf-0.99.tar.gz"
    git = "https://github.com/rst2pdf/rst2pdf.git"

    license("MIT")

    version(
        "0.100",
        sha256="3f7c6f764edf9ba4eed7ebbed361789f960f34750d71d58b543ee4acaed32ca9",
        url="https://pypi.org/packages/b0/ac/513ef4e20065eb7b18823e4340bd4fd8a3e687c522bfe3c696d1f64eed04/rst2pdf-0.100-py3-none-any.whl",
    )
    version(
        "0.99",
        sha256="5a4d032552a96de251c62ee1b926e5c5d51ef00345e9e7ce4505b9151d797cc0",
        url="https://pypi.org/packages/99/bd/bbd07a473b254bbdf3796016c2a2a16de52ed6cbb3158fb8dc5a19f22a94/rst2pdf-0.99-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@0.100:")
        depends_on("py-docutils", when="@0.99:")
        depends_on("py-importlib-metadata", when="@0.99:")
        depends_on("py-jinja2", when="@0.99:")
        depends_on("py-packaging", when="@0.99:")
        depends_on("py-pygments", when="@0.99:")
        depends_on("py-pyyaml", when="@0.99:")
        depends_on("py-reportlab", when="@0.99:")
        depends_on("py-smartypants", when="@0.99:")
