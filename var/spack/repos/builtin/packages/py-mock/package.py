# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMock(PythonPackage):
    """mock is a library for testing in Python. It allows you to replace parts
    of your system under test with mock objects and make assertions about how
    they have been used."""

    homepage = "https://github.com/testing-cabal/mock"
    pypi = "mock/mock-4.0.3.tar.gz"

    license("BSD-2-Clause")

    version(
        "4.0.3",
        sha256="122fcb64ee37cfad5b3f48d7a7d51875d7031aaf3d8be7c42e2bee25044eee62",
        url="https://pypi.org/packages/5c/03/b7e605db4a57c0f6fba744b11ef3ddf4ddebcada35022927a2b5fc623fdf/mock-4.0.3-py3-none-any.whl",
    )
    version(
        "3.0.5",
        sha256="d157e52d4e5b938c550f39eb2fd15610db062441a9c2747d3dbfa9298211d0f8",
        url="https://pypi.org/packages/05/d2/f94e68be6b17f46d2c353564da56e6fb89ef09faeeff3313a046cb810ca9/mock-3.0.5-py2.py3-none-any.whl",
    )
    version(
        "3.0.3",
        sha256="d659f8ef8810ff4c3f8f973d113a05d291a08ab0f7ed17bd60887983b93a0f9a",
        url="https://pypi.org/packages/24/15/ced6036cb01628f17cb9b8c43426b9d32ae68143221d99cd3f630bffddae/mock-3.0.3-py2.py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="5ce3c71c5545b472da17b72268978914d0252980348636840bd34a00b5cc96c1",
        url="https://pypi.org/packages/e6/35/f187bdf23be87092bd0f1200d43d23076cee4d0dec109f195173fd3ebc79/mock-2.0.0-py2.py3-none-any.whl",
    )
    version(
        "1.3.0",
        sha256="3f573a18be94de886d1191f27c168427ef693e8dcfcecf95b170577b2eb69cbb",
        url="https://pypi.org/packages/b2/50/664a70b87408bb6c14c1af2337efa64eb8d1af80c933531758b8fb41ec25/mock-1.3.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-six", when="@3.0.1:3")
