# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQuart(PythonPackage):
    """A Python ASGI web microframework with the same API as
    Flask."""

    homepage = "https://gitlab.com/pgjones/quart/"
    pypi = "Quart/Quart-0.16.3.tar.gz"

    license("MIT")

    version(
        "0.16.3",
        sha256="556d07f24a8789db3b2dca78e0fe764c5a97a75ca800b1b7e5c4cfb7c3da2ea1",
        url="https://pypi.org/packages/30/41/2405163b533eb53a7563e899d13ad5b62bfa11a7ea6b066b9f3d0a04f797/Quart-0.16.3-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@:0.18")
        depends_on("py-aiofiles")
        depends_on("py-blinker", when="@:0.18.3")
        depends_on("py-click", when="@:0.18.0")
        depends_on("py-hypercorn@0.11.2:", when="@0.15,0.16.1:")
        depends_on("py-importlib-metadata", when="@0.16:0.17 ^python@:3.7")
        depends_on("py-itsdangerous")
        depends_on("py-jinja2")
        depends_on("py-toml", when="@:0.17")
        depends_on("py-typing-extensions", when="@0.14:0.18 ^python@:3.7")
        depends_on("py-werkzeug@2.0.0:", when="@0.15,0.16.1:0.17")
