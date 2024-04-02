# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMkdocstringsPython(PythonPackage):
    """A Python handler for mkdocstrings."""

    homepage = "https://mkdocstrings.github.io/python/"
    pypi = "mkdocstrings-python/mkdocstrings-python-0.7.1.tar.gz"

    license("ISC")

    version(
        "0.7.1",
        sha256="a22060bfa374697678e9af4e62b020d990dad2711c98f7a9fac5c0345bef93c7",
        url="https://pypi.org/packages/a3/17/1fa817ea13240ef09a86a7429c12ed4fd53957e07e956f33e457122d9e8b/mkdocstrings_python-0.7.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@:1.1")
        depends_on("py-griffe@0.11.1:", when="@:0.7")
        depends_on("py-mkdocstrings@0.19:", when="@0.7:0.8")
