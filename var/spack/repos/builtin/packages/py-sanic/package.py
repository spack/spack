# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySanic(PythonPackage):
    """Sanic is a Flask-like Python 3.5+ web server that is written to go fast.
    It is based on the work done by the amazing folks at magicstack"""

    homepage = "https://github.com/huge-success/sanic"
    pypi = "sanic/sanic-20.6.3.tar.gz"

    license("MIT")

    version(
        "20.6.3",
        sha256="202b75fbf334140cffe559f18772c08263ad97e3534cda3597bc7c3446311526",
        url="https://pypi.org/packages/63/7c/df37dec6e44cee27f1d597833b1cb69d8bba3593ac2eae3e29ee4c17f1fb/sanic-20.6.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-aiofiles@0.3:", when="@:20.9")
        depends_on("py-httptools@0.0.10:")
        depends_on("py-httpx@0.11.1:0.11", when="@20:20.6")
        depends_on("py-multidict@4", when="@:19.12.2,20:20.9.0")
        depends_on("py-ujson@1.35:", when="platform=linux")
        depends_on("py-ujson@1.35:", when="platform=freebsd")
        depends_on("py-ujson@1.35:", when="platform=darwin")
        depends_on("py-ujson@1.35:", when="platform=cray")
        depends_on("py-uvloop@0.5.3:", when="@:19.12.4,20:20.12.1,20.12.4:22.9 platform=linux")
        depends_on("py-uvloop@0.5.3:", when="@:19.12.4,20:20.12.1,20.12.4:22.9 platform=freebsd")
        depends_on("py-uvloop@0.5.3:", when="@:19.12.4,20:20.12.1,20.12.4:22.9 platform=darwin")
        depends_on("py-uvloop@0.5.3:", when="@:19.12.4,20:20.12.1,20.12.4:22.9 platform=cray")
        depends_on("py-websockets@8.1:8", when="@20.6:20.12.4,21:21.3")
