# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMike(PythonPackage):
    """mike is a Python utility to easily deploy multiple versions of your
    MkDocs-powered docs to a Git branch, suitable for deploying to Github
    via gh-pages."""

    homepage = "https://github.com/jimporter/mike"
    pypi = "mike/mike-1.1.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.1.2",
        sha256="4c307c28769834d78df10f834f57f810f04ca27d248f80a75f49c6fa2d1527ca",
        url="https://pypi.org/packages/66/8a/f226f8c512a4e3ee36438613fde32d371262e985643d308850cf4bdaed15/mike-1.1.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-jinja2", when="@:1")
        depends_on("py-mkdocs@1.0:")
        depends_on("py-pyyaml@5.1:", when="@1.1:")
        depends_on("py-verspec", when="@1:")
