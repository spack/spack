# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClimax(PythonPackage):
    """ClimaX: A foundation model for weather and climate."""

    homepage = "https://github.com/microsoft/ClimaX"
    url = "https://github.com/microsoft/ClimaX/archive/refs/tags/v0.3.1.tar.gz"
    git = "https://github.com/microsoft/ClimaX.git"

    license("MIT")

    version(
        "0.3.1",
        sha256="9c13ed893aefcb03c1d34914b7aba92e0f18beadae68c1f5c83aecbad71d182c",
        url="https://pypi.org/packages/91/51/1f3d7556c06d082623d8885aaa50767b6e1c0696004c27cadedfa81832cd/climax-0.3.1-py2.py3-none-any.whl",
    )

    # pyproject.toml

    # docker/environment.yml
    # (only including deps that are actually imported, ignoring version)
