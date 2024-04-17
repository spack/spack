# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTomliW(PythonPackage):
    """A lil' TOML writer."""

    homepage = "https://github.com/hukkin/tomli-w"
    pypi = "tomli_w/tomli_w-1.0.0.tar.gz"

    license("MIT")

    version(
        "1.0.0",
        sha256="9f2a07e8be30a0729e533ec968016807069991ae2fd921a78d42f429ae5f4463",
        url="https://pypi.org/packages/bb/01/1da9c66ecb20f31ed5aa5316a957e0b1a5e786a0d9689616ece4ceaf1321/tomli_w-1.0.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@1:")
