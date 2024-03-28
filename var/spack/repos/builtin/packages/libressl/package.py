# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libressl(AutotoolsPackage):
    """LibreSSL is a version of the TLS/crypto stack forked from OpenSSL
    in 2014, with goals of modernizing the codebase, improving
    security, and applying best practice development processes."""

    homepage = "https://www.libressl.org"
    url = "https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-3.6.1.tar.gz"

    maintainers("eschnett")

    license("custom")

    version("3.7.2", sha256="b06aa538fefc9c6b33c4db4931a09a5f52d9d2357219afcbff7d93fe12ebf6f7")
    version("3.6.3", sha256="87b1bbe36e9eec8d0ae5f04c83d36b2c5b0e581784c7eb0817025ed29eadea37")
    version("3.6.1", sha256="acfac61316e93b919c28d62d53037ca734de85c46b4d703f19fd8395cf006774")

    variant("shared", default=True, description="Build shared libraries")
    variant("static", default=False, description="Build static libraries")

    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable("shared"))
        args.extend(self.enable_or_disable("static"))
        return args
