# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyUvicorn(PythonPackage):
    """The lightning-fast ASGI server."""

    homepage = "https://www.uvicorn.org/"
    pypi = "uvicorn/uvicorn-0.20.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.20.0",
        sha256="c3ed1598a5668208723f2bb49336f4509424ad198d6ab2615b7783db58d919fd",
        url="https://pypi.org/packages/96/f3/f39ac8ac3bdf356b4934b8f7e56173e96681f67ef0cd92bd33a5059fae9e/uvicorn-0.20.0-py3-none-any.whl",
    )

    variant("standard", default=False, description="Build standard dependencies")

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@:0.22")
        depends_on("py-click@7:")
        depends_on("py-colorama@0.4:", when="+standard platform=windows")
        depends_on("py-h11@0.8:")
        depends_on("py-httptools@0.5:", when="@0.19:+standard")
        depends_on("py-python-dotenv@0.13:", when="+standard")
        depends_on("py-pyyaml@5.1:", when="+standard")
        depends_on("py-typing-extensions", when="@:0.22 ^python@:3.7")
        depends_on("py-uvloop@0.14.0:0.14,0.15.2:", when="+standard platform=linux")
        depends_on("py-uvloop@0.14.0:0.14,0.15.2:", when="+standard platform=freebsd")
        depends_on("py-uvloop@0.14.0:0.14,0.15.2:", when="+standard platform=darwin")
        depends_on("py-uvloop@0.14.0:0.14,0.15.2:", when="+standard platform=cray")
        depends_on("py-watchfiles@0.13:", when="@0.18:+standard")
        depends_on("py-websockets@10.4:", when="@0.20:+standard")
