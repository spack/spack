# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestMypy(PythonPackage):
    """Mypy static type checker plugin for Pytest."""

    homepage = "https://github.com/dbader/pytest-mypy"
    pypi = "pytest-mypy/pytest-mypy-0.4.2.tar.gz"

    license("MIT")

    version(
        "0.4.2",
        sha256="3b7b56912d55439d5f447cc609f91caac7f74f0f1c89f1379d04f06bac777c32",
        url="https://pypi.org/packages/9c/57/8f7cf30df4774fa77a9bb61c9a41e793bcd1813753dd815ae064fe9342cf/pytest_mypy-0.4.2-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@:3", when="@0.3.3:0.6")
        depends_on("py-mypy@0.501:", when="@0.4.2: ^python@:3.7")
        depends_on("py-mypy@0.700:", when="@0.4.2:0.7 ^python@3.8:")
        depends_on("py-pytest@2.8:", when="@0.3.3:0.4")
