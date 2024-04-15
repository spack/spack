# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPytestTimeout(PythonPackage):
    """A plugin which will terminate tests after a certain timeout,
    assuming the test session isn't being debugged."""

    homepage = "https://github.com/pytest-dev/pytest-timeout/"
    pypi = "pytest-timeout/pytest-timeout-1.4.2.tar.gz"

    license("MIT")

    version(
        "2.2.0",
        sha256="bde531e096466f49398a59f2dde76fa78429a09a12411466f88a07213e220de2",
        url="https://pypi.org/packages/e2/3e/abfdb7319d71a179bb8f5980e211d93e7db03f0c0091794dbcd652d642da/pytest_timeout-2.2.0-py3-none-any.whl",
    )
    version(
        "1.4.2",
        sha256="541d7aa19b9a6b4e475c759fd6073ef43d7cdc9a92d95644c260076eb257a063",
        url="https://pypi.org/packages/46/df/97cc0b5b8b53da0e265acd0aeecfc0c279e950a029acd2d7b4e54b00b25f/pytest_timeout-1.4.2-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@2.2:")
        depends_on("py-pytest@5:", when="@2:2.2")
        depends_on("py-pytest@3.6:", when="@1.3:1")
