# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OphidiaServer(AutotoolsPackage):
    """Front-end server of the Ophidia framework"""

    homepage = "https://github.com/SoniaScard/ophidia-server"
    url = "https://github.com/SoniaScard/ophidia-server/archive/refs/tags/v1.7.2.tar.gz"
    maintainers("eldoo", "SoniaScard")
    version("1.7.2", sha256="452587775343b266bbb5adcfeee64e7f7e9a9bbfcb2133646a831ae3e74348be")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkg-config", type="build")

    depends_on("libmatheval")
    depends_on("jansson")
    depends_on("libxml2")
    depends_on("libssh2")
    depends_on("openssl")
    depends_on("mysql")
    depends_on("curl")
    depends_on("ophidia-analytics-framework")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = [
            "--with-web-server-path={0}/html".format(
                self.spec["ophidia-analytics-framework"].prefix
            ),
            "--with-web-server-url=http://127.0.0.1/ophidia",
            "--with-framework-path={0}".format(self.spec["ophidia-analytics-framework"].prefix),
        ]

        return args
