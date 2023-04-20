# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XmlrpcC(AutotoolsPackage):
    """Programming library for writing an XML-RPC server or client in
    C or C++."""

    homepage = "https://sourceforge.net/projects/xmlrpc-c/"
    url = "https://sourceforge.net/projects/xmlrpc-c/files/Xmlrpc-c%20Super%20Stable/1.51.06/xmlrpc-c-1.51.06.tgz"

    version("1.51.06", sha256="06dcd87d9c88374559369ffbe83b3139cf41418c1a2d03f20e08808085f89fd0")

    variant("curl", default=False, description="Build the XMLRPC curl client")
    depends_on("curl", when="+curl")

    def configure_args(self):
        variants = self.spec.variants

        args = []

        if variants["curl"].value:
            args.append("--enable-curl-client")

        if self.spec.target.family == "aarch64":
            args.append("--build=arm-linux")

        return args
