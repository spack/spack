# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttpx(PythonPackage):
    """HTTPX is a fully featured HTTP client for Python 3, which provides sync
    and async APIs, and support for both HTTP/1.1 and HTTP/2."""

    homepage = "https://github.com/encode/httpx"
    pypi = "httpx/httpx-0.15.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.23.3",
        sha256="a211fcce9b1254ea24f0cd6af9869b3d29aba40154e947d2a07bb499b3e310d6",
        url="https://pypi.org/packages/ac/a2/0260c0f5d73bdf06e8d3fc1013a82b9f0633dc21750c9e3f3cb1dba7bb8c/httpx-0.23.3-py3-none-any.whl",
    )
    version(
        "0.22.0",
        sha256="e35e83d1d2b9b2a609ef367cc4c1e66fd80b750348b20cc9e19d1952fc2ca3f6",
        url="https://pypi.org/packages/2f/d3/6a990516a43a522a72da356c4a91c03e09c0cddce8106e7e1215c120011f/httpx-0.22.0-py3-none-any.whl",
    )
    version(
        "0.15.2",
        sha256="a2bd6eb6d52f0fbd3b082fc8a37b1f50d6112352a83aa04a60f4107f723b018e",
        url="https://pypi.org/packages/fc/2c/edea45026079eb4c790aed3d40eea7f0bca199f5f82358d2407cc467efe7/httpx-0.15.2-py3-none-any.whl",
    )
    version(
        "0.11.1",
        sha256="1d3893d3e4244c569764a6bae5c5a9fbbc4a6ec3825450b5696602af7a275576",
        url="https://pypi.org/packages/46/a9/36b9e193567d879e2da3dd57c755bdf12aa4c2485b1a4610c5799f387ae5/httpx-0.11.1-py2.py3-none-any.whl",
    )

    variant("http2", default=False, when="@0.15.2:", description="Enable http2 support")

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.23:0.24")
        depends_on("py-async-generator", when="@0.18:0.22,1: ^python@:3.6")
        depends_on("py-certifi")
        depends_on("py-chardet@3", when="@:0.14")
        depends_on("py-charset-normalizer", when="@0.19:0.22,1:")
        depends_on("py-h11@0.8:0.9", when="@0.10:0.12")
        depends_on("py-h2@3:", when="@0.19:+http2")
        depends_on("py-h2@3", when="@0.14:0.18+http2")
        depends_on("py-h2@3", when="@:0.12")
        depends_on("py-hstspreload", when="@0.9:0.13")
        depends_on("py-httpcore@0.15:0.16", when="@0.23.1:0.23")
        depends_on("py-httpcore@0.14.5:0.14", when="@0.22")
        depends_on("py-httpcore@0.11", when="@0.15")
        depends_on("py-idna@2", when="@:0.14.1")
        depends_on("py-rfc3986@1.3:1+idna2008", when="@0.14.2:0.23,1:")
        depends_on("py-rfc3986@1.3:1", when="@0.9:0.14.1")
        depends_on("py-sniffio", when="@0.13.0:")
        depends_on("py-sniffio@1:", when="@0.9:0.12")
        depends_on("py-urllib3@1", when="@0.11:0.12")

    # Historical dependencies
