# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBranca(PythonPackage):
    """Generate complex HTML+JS pages with Python."""

    homepage = "https://python-visualization.github.io/branca"
    pypi = "branca/branca-0.7.1.tar.gz"

    license("MIT")

    version(
        "0.7.1",
        sha256="70515944ed2d1ed2784c552508df58037ca19402a8a1069d57f9113e3e012f51",
        url="https://pypi.org/packages/17/ce/14166d0e273d12065516625fb02426350298e7b4ba59198b5fe454b46202/branca-0.7.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.6:")
        depends_on("py-jinja2@3.0.0:", when="@0.7.1:")
