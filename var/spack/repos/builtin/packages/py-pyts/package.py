# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyts(PythonPackage):
    """pyts is a Python package for time series classification. It aims to make
    time series classification easily accessible by providing preprocessing and
    utility tools, and implementations of state-of-the-art algorithms. Most of
    these algorithms transform time series, thus pyts provides several tools to
    perform these transformations."""

    homepage = "https://github.com/johannfaouzi/pyts"
    pypi = "pyts/pyts-0.12.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.12.0",
        sha256="acd66b0cf1fd17d9ce6449335f5da30701f65fdee185d4b918726b62ca6af79d",
        url="https://pypi.org/packages/55/6e/fedefe4a1564943824e2dc4baa4cc5ed0862a4fe25ea3b69b4e3b9134bcf/pyts-0.12.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-joblib@0.12:", when="@0.11:0.12")
        depends_on("py-numba@0.48:", when="@0.11:0.12")
        depends_on("py-numpy@1.17.5:", when="@0.11:0.12")
        depends_on("py-scikit-learn@0.22.1:", when="@0.11:0.12")
        depends_on("py-scipy@1.3.0:", when="@0.11:0.12")
