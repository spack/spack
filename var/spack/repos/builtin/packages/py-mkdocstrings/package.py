# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMkdocstrings(PythonPackage):
    """Automatic documentation from sources, for MkDocs."""

    homepage = "https://mkdocstrings.github.io/"
    pypi = "mkdocstrings/mkdocstrings-0.19.0.tar.gz"

    license("ISC")

    version(
        "0.19.0",
        sha256="3217d510d385c961f69385a670b2677e68e07b5fea4a504d86bf54c006c87c7d",
        url="https://pypi.org/packages/60/53/eedad37654a74f969d297e0dec67db17e7e013266cc6e3ea61c7568a01c8/mkdocstrings-0.19.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.18:0.22")
        depends_on("py-jinja2@2.11.1:", when="@0.17:")
        depends_on("py-markdown@3.3:", when="@0.17:")
        depends_on("py-markupsafe@1.1:", when="@0.17:")
        depends_on("py-mkdocs@1.2:", when="@0.17:0.23")
        depends_on("py-mkdocs-autorefs@0.3.1:", when="@0.18:")
        depends_on("py-pymdown-extensions@6.3:", when="@0.17:")
