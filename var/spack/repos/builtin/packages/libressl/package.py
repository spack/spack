# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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

    version("3.6.1", sha256="acfac61316e93b919c28d62d53037ca734de85c46b4d703f19fd8395cf006774")

    variant("shared", default=True, description="Build shared libraries")
    variant("static", default=False, description="Build static libraries")

    def configure_args(self):
        args = [
            "--enable-shared" if "+shared" in spec else "--disable-shared",
            "--enable-static" if "+static" in spec else "--disable-static",
        ]
        return args
