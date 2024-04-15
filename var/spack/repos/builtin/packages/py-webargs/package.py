# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWebargs(PythonPackage):
    """Python library for parsing and validating HTTP request objects,
    with built-in support for popular web frameworks, including Flask,
    Django, Bottle, Tornado, Pyramid, Falcon, and aiohttp."""

    homepage = "https://github.com/marshmallow-code/webargs"
    pypi = "webargs/webargs-8.1.0.tar.gz"

    maintainers("haralmha")

    license("MIT")

    version(
        "8.1.0",
        sha256="8d4025a5efcfe15cc385e39bd84167d3e9ede0eb485e246eec21f340f1a0caf9",
        url="https://pypi.org/packages/96/67/1e4d9caaf7c78ef279ecf37c168c62322e685fd4bf16cc3158f127fbf598/webargs-8.1.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@8.1:8.3")
        depends_on("py-marshmallow@3.0.0:", when="@7:")
        depends_on("py-packaging", when="@8.1:")
