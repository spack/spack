# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttpx(PythonPackage):
    """HTTPX is a fully featured HTTP client for Python 3, which provides sync
    and async APIs, and support for both HTTP/1.1 and HTTP/2."""

    homepage = "https://github.com/encode/httpx"
    pypi = "httpx/httpx-0.15.2.tar.gz"

    version("0.22.0", sha256="d8e778f76d9bbd46af49e7f062467e3157a5a3d2ae4876a4bbfd8a51ed9c9cb4")
    version("0.15.2", sha256="713a2deaf96d85bbd4a1fbdf0edb27d6b4ee2c9aaeda8433042367e4b9e1628d")
    version("0.11.1", sha256="7d2bfb726eeed717953d15dddb22da9c2fcf48a4d70ba1456aa0a7faeda33cf7")

    variant("http2", default=False, when="@0.15.2:", description="Enable http2 support")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-certifi", type=("build", "run"))
    depends_on("py-charset-normalizer", type=("build", "run"), when="@0.22.0:")

    depends_on("py-httpcore@0.11.0:0.11", type=("build", "run"), when="@0.15.2")
    depends_on("py-httpcore@0.14.5:0.14", type=("build", "run"), when="@0.22.0:")

    depends_on("py-sniffio@1.0:1", type=("build", "run"), when="@0.11.1")
    depends_on("py-sniffio", type=("build", "run"), when="@0.15.2:")

    depends_on("py-rfc3986@1.3:1", type=("build", "run"), when="@0.11.1")
    depends_on("py-rfc3986+idna2008@1.3:1", type=("build", "run"), when="@0.15.2:")

    depends_on("py-h2@3.0:3", type=("build", "run"), when="@0.11.1")
    depends_on("py-h2@3.0:3", type=("build", "run"), when="@0.15.2+http2")
    depends_on("py-h2@3.0:4", type=("build", "run"), when="@0.22.0:+http2")

    # Version 0.11.1 only dependencies
    depends_on("py-hstspreload", type=("build", "run"), when="@0.11.1")
    depends_on("py-chardet@3.0:3", type=("build", "run"), when="@0.11.1")
    depends_on("py-h11@0.8:0.9", type=("build", "run"), when="@0.11.1")
    depends_on("py-idna@2.0:2", type=("build", "run"), when="@0.11.1")
    depends_on("py-urllib3@1.0:1", type=("build", "run"), when="@0.11.1")
