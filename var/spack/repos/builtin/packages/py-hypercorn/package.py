# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHypercorn(PythonPackage):
    """A ASGI Server based on Hyper libraries and inspired by
    Gunicorn."""

    homepage = "https://gitlab.com/pgjones/hypercorn/"
    pypi = "Hypercorn/Hypercorn-0.13.2.tar.gz"

    license("MIT")

    version(
        "0.13.2",
        sha256="ca18f91ab3fa823cbe9e949738f9f2cc07027cd647c80d8f93e4b1a2a175f112",
        url="https://pypi.org/packages/c9/28/79bbca7d9218d37f8888a0f3215e7ba03851d1c77c11d841542e33cc3190/Hypercorn-0.13.2-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@:0.15")
        depends_on("py-h11")
        depends_on("py-h2@3.1:")
        depends_on("py-priority")
        depends_on("py-toml", when="@:0.14.3")
        depends_on("py-typing-extensions@3.7.4:", when="@0.12:0.14 ^python@:3.7")
        depends_on("py-wsproto@0.14:")
