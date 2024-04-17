# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMkdocsAutorefs(PythonPackage):
    """Automatically link across pages in MkDocs."""

    homepage = "https://mkdocstrings.github.io/autorefs/"
    pypi = "mkdocs-autorefs/mkdocs-autorefs-0.4.1.tar.gz"

    license("ISC")

    version(
        "0.4.1",
        sha256="a2248a9501b29dc0cc8ba4c09f4f47ff121945f6ce33d760f145d6f89d313f5b",
        url="https://pypi.org/packages/fb/5c/6594400290df38f99bf8d9ef249387b56f4ad962667836266f6fe7da8597/mkdocs_autorefs-0.4.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.4")
        depends_on("py-markdown@3.3:", when="@0.4:")
        depends_on("py-mkdocs@1.1:", when="@0.4:")
