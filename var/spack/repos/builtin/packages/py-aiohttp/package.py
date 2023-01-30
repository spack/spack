# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAiohttp(PythonPackage):
    """Supports both client and server side of HTTP protocol.
    Supports both client and server Web-Sockets out-of-the-box and
    avoids Callbacks.  Provides Web-server with middlewares and
    plugable routing."""

    homepage = "https://github.com/aio-libs/aiohttp"
    pypi = "aiohttp/aiohttp-3.8.1.tar.gz"

    version("3.8.1", sha256="fc5471e1a54de15ef71c1bc6ebe80d4dc681ea600e68bfd1cbce40427f0b7578")
    version("3.8.0", sha256="d3b19d8d183bcfd68b25beebab8dc3308282fe2ca3d6ea3cb4cd101b3c279f8d")
    version("3.7.4", sha256="5d84ecc73141d0a0d61ece0742bb7ff5751b0657dab8405f899d3ceb104cc7de")
    version("3.6.2", sha256="259ab809ff0727d0e834ac5e8a283dc5e3e0ecc30c4d80b3cd17a4139ce1f326")

    depends_on("py-setuptools@46.4:", type="build")
    depends_on("py-charset-normalizer@2.0:2", type=("build", "run"), when="@3.8.0:")
    depends_on("python@3.5.3:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@3.7:")
    depends_on("py-attrs@17.3.0:", type=("build", "run"))
    depends_on("py-chardet@2.0:3", type=("build", "run"), when="@:3.7")
    depends_on("py-multidict@4.5:4", type=("build", "run"), when="@:3.6.2")
    depends_on("py-multidict@4.5:6", type=("build", "run"), when="@3.6.3:")
    depends_on("py-async-timeout@3.0:3", type=("build", "run"), when="@:3.7.4")
    depends_on("py-async-timeout@4.0:4", type=("build", "run"), when="@3.8.0:")
    depends_on("py-asynctest@0.13.0", type=("build", "run"), when="@3.8.0: ^python@:3.7")
    depends_on("py-yarl@1.0:1", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", type=("build", "run"), when="@3.8: ^python@:3.7")
    depends_on("py-typing-extensions@3.6.5:", type=("build", "run"), when="@3.7")
    depends_on("py-typing-extensions@3.6.5:", type=("build", "run"), when="@:3.6 ^python@:3.7")
    depends_on("py-frozenlist@1.1.1:", type=("build", "run"), when="@3.8.1:")
    depends_on("py-aiosignal@1.1.2:", type=("build", "run"), when="@3.8.1:")
