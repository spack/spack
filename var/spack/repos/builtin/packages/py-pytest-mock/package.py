# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestMock(PythonPackage):
    """Thin-wrapper around the mock package for easier use with py.test"""

    homepage = "https://github.com/pytest-dev/pytest-mock"
    pypi = "pytest-mock/pytest-mock-1.11.1.tar.gz"

    maintainers("thomas-bouvier")

    license("MIT")

    version(
        "3.10.0",
        sha256="f4c973eeae0282963eb293eb173ce91b091a79c1334455acfac9ddee8a1c784b",
        url="https://pypi.org/packages/91/84/c951790e199cd54ddbf1021965b62a5415b81193ebdb4f4af2659fd06a73/pytest_mock-3.10.0-py3-none-any.whl",
    )
    version(
        "1.11.1",
        sha256="34520283d459cdf1d0dbb58a132df804697f1b966ecedf808bbf3d255af8f659",
        url="https://pypi.org/packages/ca/04/c530b2e4d61f99c524dcac0a9002563955370622f70fe4771cd4e56e217b/pytest_mock-1.11.1-py2.py3-none-any.whl",
    )
    version(
        "1.2",
        sha256="2911668c5ea518a07e2da53a170e2f86eaccf1245ec9605c37eadf6578dec468",
        url="https://pypi.org/packages/6a/40/d5f2fbef42f85b8c53ddb2bb1db847ef46c86e6204abfeaa605b3ed07307/pytest_mock-1.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@3.7:3.11")
        depends_on("py-pytest@5:", when="@3.3:")
        depends_on("py-pytest@2.7:", when="@1.6.1,1.6.3:3.2")
