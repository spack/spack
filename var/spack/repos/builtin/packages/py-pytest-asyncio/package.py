# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestAsyncio(PythonPackage):
    """pytest-asyncio is an Apache2 licensed library, written in Python,
    for testing asyncio code with pytest."""

    homepage = "https://github.com/pytest-dev/pytest-asyncio"
    pypi = "pytest-asyncio/pytest-asyncio-0.18.3.tar.gz"

    license("Apache-2.0")

    version(
        "0.23.5",
        sha256="4e7093259ba018d58ede7d5315131d21923a60f8a6e9ee266ce1589685c89eac",
        url="https://pypi.org/packages/ce/0c/a60bcaeb3ba2f938b4d76e535180ea9f43e8da5fa6933fd9401f6f6e46ae/pytest_asyncio-0.23.5-py3-none-any.whl",
    )
    version(
        "0.18.3",
        sha256="16cf40bdf2b4fb7fc8e4b82bd05ce3fbcd454cbf7b92afc445fe299dabb88213",
        url="https://pypi.org/packages/8b/d6/4ecdd0c5b49a2209131b6af78baa643cec35f213abbc54d0eb1542b3786d/pytest_asyncio-0.18.3-1-py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="a962e8e1b6ec28648c8fe214edab4e16bacdb37b52df26eb9d63050af309b2a9",
        url="https://pypi.org/packages/33/7f/2ed9f460872ebcc62d30afad167673ca10df36ff56a6f6df2f1d3671adc8/pytest_asyncio-0.9.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.22:")
        depends_on("python@3.7:", when="@0.17:0.21")
        depends_on("py-pytest@7.0.0:", when="@0.23.5-alpha0:")
        depends_on("py-pytest@6.1:", when="@0.17.1:0.20")
        depends_on("py-pytest@3.0.6:", when="@0.6:0.10")
        depends_on("py-typing-extensions@3.7:", when="@0.18:0.21 ^python@:3.7")
