# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NetSnmp(AutotoolsPackage):
    """A SNMP application library, tools and daemon."""

    homepage = "http://www.net-snmp.org/"
    url = "https://sourceforge.net/projects/net-snmp/files/net-snmp/5.9.1/net-snmp-5.9.1.tar.gz/download"

    version("5.9.1", sha256="eb7fd4a44de6cddbffd9a92a85ad1309e5c1054fb9d5a7dd93079c8953f48c3f")
    version("5.9", sha256="04303a66f85d6d8b16d3cc53bde50428877c82ab524e17591dfceaeb94df6071")

    depends_on("perl-extutils-makemaker")
    depends_on("ncurses")

    def configure_args(self):
        args = ["--with-defaults", "LIBS=-ltinfo"]
        return args

    def install(self, spec, prefix):
        make("install", parallel=False)
