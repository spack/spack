# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTyper(PythonPackage):
    """Typer, build great CLIs. Easy to code. Based on Python type hints."""

    homepage = "https://github.com/tiangolo/typer"
    pypi = "typer/typer-0.9.0.tar.gz"

    license("MIT")

    version(
        "0.9.0",
        sha256="5d96d986a21493606a358cae4461bd8cdf83cbf33a5aa950ae629ca3b51467ee",
        url="https://pypi.org/packages/bf/0e/c68adf10adda05f28a6ed7b9f4cd7b8e07f641b44af88ba72d9c89e4de7a/typer-0.9.0-py3-none-any.whl",
    )
    version(
        "0.7.0",
        sha256="b5e704f4e48ec263de1c0b3a2387cd405a13767d2f907f44c1a08cbad96f606d",
        url="https://pypi.org/packages/0d/44/56c3f48d2bb83d76f5c970aef8e2c3ebd6a832f09e3621c5395371fe6999/typer-0.7.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-click@7.1.1:", when="@0.4:0.10")
        depends_on("py-typing-extensions@3.7.4.3:", when="@0.9:0.11,0.12.1:")
