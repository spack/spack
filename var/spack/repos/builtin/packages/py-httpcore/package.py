# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttpcore(PythonPackage):
    """The HTTP Core package provides a minimal low-level HTTP client,
    which does one thing only. Sending HTTP requests."""

    homepage = "https://github.com/encode/httpcore"
    pypi = "httpcore/httpcore-0.11.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.16.3",
        sha256="da1fb708784a938aa084bde4feb8317056c55037247c787bd7e19eb2c2949dc0",
        url="https://pypi.org/packages/04/7e/ef97af4623024e8159993b3114ce208de4f677098ae058ec5882a1bf7605/httpcore-0.16.3-py3-none-any.whl",
    )
    version(
        "0.14.7",
        sha256="47d772f754359e56dd9d892d9593b6f9870a37aeb8ba51e9a88b09b3d68cfade",
        url="https://pypi.org/packages/e7/38/7b76d3d71c462dc936e333b358a3106e7af913e6c8c9dd5a45684fec08cc/httpcore-0.14.7-py3-none-any.whl",
    )
    version(
        "0.11.0",
        sha256="7a6804b18e1b8fc61ec4df868cb5c679d225fffbb81e48455ee9b57792cc3ac6",
        url="https://pypi.org/packages/64/fe/a9db014f98e0bb0c40d62dfee8b265f4e3a959da5daa672f68191776e523/httpcore-0.11.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.15:0.17")
        depends_on("py-anyio@3.0.0:", when="@0.16:0")
        depends_on("py-anyio@3", when="@0.13.4:0.15")
        depends_on("py-certifi", when="@0.14.1:")
        depends_on("py-h11@0.13:", when="@0.16:")
        depends_on("py-h11@0.11:0.12", when="@0.13.3:0.15")
        depends_on("py-h11@0.8:0.9", when="@:0.11")
        depends_on("py-sniffio@1:", when="@:0")
