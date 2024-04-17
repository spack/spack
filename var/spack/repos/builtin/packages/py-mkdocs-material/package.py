# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMkdocsMaterial(PythonPackage):
    """Write your documentation in Markdown and create a professional static
    site for your Open Source or commercial project in minutes."""

    homepage = "https://squidfunk.github.io/mkdocs-material/"
    pypi = "mkdocs-material/mkdocs-material-8.4.0.tar.gz"

    license("MIT")

    version(
        "8.4.0",
        sha256="ef6641e1910d4f217873ac376b4594f3157dca3949901b88b4991ba8e5477577",
        url="https://pypi.org/packages/b8/be/e2f9f868d64d2147dd641eda9216e0f86ce5b3111a2be63a07cc1bc55520/mkdocs_material-8.4.0-py2.py3-none-any.whl",
    )
    version(
        "8.3.6",
        sha256="01f3fbab055751b3b75a64b538e86b9ce0c6a0f8d43620f6287dfa16534443e5",
        url="https://pypi.org/packages/cb/bf/501a3aa2e67f9d35dfd6c1882dc62c53b6bb4dc2110f7d49c1df45d40b92/mkdocs_material-8.3.6-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@:9.2")
        depends_on("py-jinja2@3.0.2:", when="@8.3.1:9.0.0-beta4")
        depends_on("py-markdown@3.2:", when="@:9.2.6")
        depends_on("py-mkdocs@1.3:", when="@:8.5.4")
        depends_on("py-mkdocs-material-extensions@1.0.3:", when="@:8.5.7")
        depends_on("py-pygments@2.12:", when="@:9.0.0-beta4")
        depends_on("py-pymdown-extensions@9.4:", when="@:8")
