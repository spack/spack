# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AmqpCpp(CMakePackage):
    """AMQP-CPP is a C++ library for communicating with a RabbitMQ message
    broker. The library can be used to parse incoming data from, and generate
    frames to, a RabbitMQ server."""

    homepage = "https://github.com/CopernicaMarketingSoftware/AMQP-CPP"
    git = "https://github.com/CopernicaMarketingSoftware/AMQP-CPP.git"
    url = "https://github.com/CopernicaMarketingSoftware/AMQP-CPP/archive/refs/tags/v4.3.19.tar.gz"

    maintainers("lpottier")

    version("4.3.19", sha256="ca29bb349c498948576a4604bed5fd3c27d87240b271a4441ccf04ba3797b31d")

    variant(
        "tcp",
        default=False,
        description="Build TCP module. TCP module is supported for Linux only.",
    )
    variant("shared", default=True, description="Build as a shared library (static by default)")

    conflicts("tcp", when="platform=darwin", msg="TCP module requires Linux")

    depends_on("cmake@3.5:", type="build")
    depends_on("openssl@1.1.1:", when="+tcp", type=("build", "link", "run"))

    def cmake_args(self):
        args = [
            self.define_from_variant("AMQP-CPP_LINUX_TCP", "tcp"),
            self.define_from_variant("AMQP-CPP_BUILD_SHARED", "shared"),
        ]
        return args
