# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Crow(CMakePackage):
    """Crow is a C++ microframework for creating HTTP and WebSocket services.  It uses routing
    similar to Python's Flask, which makes it easy to use.  It is also extremely fast, beating
    many other C++ and non-C++ web frameworks."""

    homepage = "https://crowcpp.org"
    url = "https://github.com/CrowCpp/Crow/archive/refs/tags/v1.2.1.2.tar.gz"

    maintainers("ta7mid")

    license("BSD-3-Clause")

    version("1.2.1.2", sha256="dc008515f64c9054250909a16bf0d9173af845d2c6d4e49ed6d3f0f32dfdc747")
    version("1.2.0", sha256="c80d0b23c6a20f8aa6fe776669dc8a9fb984046891d2f70bfc0539d16998164b")

    variant(
        "asio",
        default="standalone",
        description="Asio implementation to use",
        values=("standalone", "boost"),
    )
    variant(
        "ssl",
        default=False,
        description="Enable support for HTTPS and WebSocket Secure using OpenSSL",
    )
    variant(
        "compression", default=False, description="Enable support for HTTP compression using zlib"
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("asio", when="asio=standalone")
    depends_on("boost+system+date_time", when="asio=boost")
    depends_on("openssl", when="+ssl")
    depends_on("zlib", when="+compression")

    def cmake_args(self):
        return [
            "-DCROW_BUILD_EXAMPLES:BOOL=OFF",
            "-DCROW_BUILD_TESTS:BOOL=OFF",
            self.define("CROW_USE_BOOST", self.spec.satisfies("asio=boost")),
            self.define_from_variant("CROW_ENABLE_SSL", "ssl"),
            self.define_from_variant("CROW_ENABLE_COMPRESSION", "compression"),
        ]
