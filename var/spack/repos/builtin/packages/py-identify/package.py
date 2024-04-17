# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIdentify(PythonPackage):
    """File identification library for Python.

    Given a file (or some information about a file), return a set of
    standardized tags identifying what the file is."""

    homepage = "https://github.com/pre-commit/identify"
    pypi = "identify/identify-1.4.7.tar.gz"

    license("MIT")

    version(
        "2.5.24",
        sha256="986dbfb38b1140e763e413e6feb44cd731faf72d1909543178aa79b0e258265d",
        url="https://pypi.org/packages/4f/fd/2c46fba2bc032ba4c970bb8de59d25187087d7138a0ebf7c1dcc91d94f01/identify-2.5.24-py2.py3-none-any.whl",
    )
    version(
        "2.5.5",
        sha256="ef78c0d96098a3b5fe7720be4a97e73f439af7cf088ebf47b620aeaa10fadf97",
        url="https://pypi.org/packages/fd/80/681ca4485f8cefe72ee43b9a0b0c15f7a78642c6c187d5e4bed8421cc576/identify-2.5.5-py2.py3-none-any.whl",
    )
    version(
        "2.5.3",
        sha256="25851c8c1370effb22aaa3c987b30449e9ff0cece408f810ae6ce408fdd20893",
        url="https://pypi.org/packages/0c/ed/ee58d0ae16c7407762171c493db655b19b68c40d15b4294ef5d827ee33ea/identify-2.5.3-py2.py3-none-any.whl",
    )
    version(
        "1.4.7",
        sha256="4f1fe9a59df4e80fcb0213086fcf502bc1765a01ea4fe8be48da3b65afd2a017",
        url="https://pypi.org/packages/87/e4/66e3c82550017d3ee03c9f216e0c3dbf1c8c580c567777537adce8823597/identify-1.4.7-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@2.4.5:2.5.24")
