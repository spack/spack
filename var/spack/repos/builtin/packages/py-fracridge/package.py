# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFracridge(PythonPackage):
    """Fractional Ridge Regression."""

    homepage = "https://nrdg.github.io/fracridge"
    pypi = "fracridge/fracridge-1.4.3.tar.gz"
    git = "https://github.com/nrdg/fracridge"

    license("BSD-2-Clause")

    version(
        "2.0",
        sha256="48ef1687aaf220f6c4835f223dcf32af72706ff0b9539ef1fb8d2278c482a006",
        url="https://pypi.org/packages/10/b5/06fd8c80ae2b8a440f35324508fd482c185eed02afa111840df62c22bc43/fracridge-2.0-py3-none-any.whl",
    )
    version(
        "1.4.3",
        sha256="0db162286c0ac508b563c6f4fa2157c20327a96e39321a7802bfab9afa81bfeb",
        url="https://pypi.org/packages/f3/79/5d565bdf67512971bc92f762be8b4234c4742b8c579622cdccfffa3359df/fracridge-1.4.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2:")
        depends_on("py-numba")
        depends_on("py-pillow")
        depends_on("py-scikit-learn@0.23.2:0.23", when="@1.3.2:1")
        depends_on("py-scikit-learn", when="@:1.3.1,2:")
        depends_on("py-setuptools-scm")
