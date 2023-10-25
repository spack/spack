# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mailutils(AutotoolsPackage):
    """Mailutils is a swiss army knife of electronic mail handling.
    It offers a rich set of utilities and daemons for processing e-mail."""

    homepage = "https://mailutils.org/"
    url = "https://ftp.gnu.org/gnu/mailutils/mailutils-3.13.tar.gz"

    maintainers = ["cosmicexplorer"]

    version("3.13", sha256="41234389452805e5a47cec4fd57c61feee0cdaa6de94d0ded0cd33e778f58de2")

    variant("gdbm", default=False, description="Build with gnu DBM support")
    variant("berkeley-db", default=False, description="Build with berkeley DB support")
    variant("guile", default=False, description="Build with guile support")

    depends_on("libiconv")
    depends_on("gettext")
    depends_on("readline")
    depends_on("gnutls")
    depends_on("gdbm", when="+gdbm")
    depends_on("berkeley-db", when="+berkeley-db")
    depends_on("guile", when="+guile")
    depends_on("m4", type="build")
    depends_on("texinfo", type="build")
    depends_on("ncurses+termlib")

    def configure_args(self):
        args = ["LIBS=-ltinfo"]

        args += self.with_or_without("dbm", variant="gdbm")
        args += self.with_or_without("gdbm")
        args += self.with_or_without("berkeley-db")
        args += self.with_or_without("guile")

        return args
