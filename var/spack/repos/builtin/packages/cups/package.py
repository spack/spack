# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cups(AutotoolsPackage):
    """CUPS is the standards-based, open source printing system developed by
    Apple Inc. for macOS and other UNIX-like operating systems. CUPS uses the
    Internet Printing Protocol (IPP) to support printing to local and network
    printers. This provides the core CUPS libraries, not a complete CUPS
    install."""

    homepage = "https://www.cups.org/"
    url = "https://github.com/apple/cups/releases/download/v2.2.3/cups-2.2.3-source.tar.gz"

    license("Apache-2.0")

    version("2.3.3", sha256="261fd948bce8647b6d5cb2a1784f0c24cc52b5c4e827b71d726020bcc502f3ee")
    version("2.2.3", sha256="66701fe15838f2c892052c913bde1ba106bbee2e0a953c955a62ecacce76885f")

    depends_on("gnutls")
    depends_on("pkgconfig", type="build")

    def configure_args(self):
        args = ["--enable-gnutls", "--with-components=core"]
        return args
