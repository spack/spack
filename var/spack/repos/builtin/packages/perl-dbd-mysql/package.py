# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDbdMysql(PerlPackage):
    """MySQL driver for the Perl5 Database Interface (DBI)"""

    homepage = "https://metacpan.org/pod/DBD::mysql"
    url = "https://search.cpan.org/CPAN/authors/id/M/MI/MICHIELB/DBD-mysql-4.043.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version(
        "5.005",
        sha256="1558c203b3911e273d3f83249535b312165be2ca8edba6b6c210645d769d0541",
        url="https://cpan.metacpan.org/authors/id/D/DV/DVEEDEN/DBD-mysql-5.005.tar.gz",
    )
    version(
        "4.052",
        sha256="a83f57af7817787de0ef56fb15fdfaf4f1c952c8f32ff907153b66d2da78ff5b",
        url="https://cpan.metacpan.org/authors/id/D/DV/DVEEDEN/DBD-mysql-4.052.tar.gz",
    )

    version(
        "4.050",
        sha256="4f48541ff15a0a7405f76adc10f81627c33996fbf56c95c26c094444c0928d78",
        url="https://cpan.metacpan.org/authors/id/D/DV/DVEEDEN/DBD-mysql-4.050.tar.gz",
    )
    version("4.043", sha256="629f865e8317f52602b2f2efd2b688002903d2e4bbcba5427cb6188b043d6f99")

    depends_on("perl-devel-checklib", type="build", when="@4.050:")
    depends_on("perl-test-deep", type=("build", "run"))
    depends_on("perl-dbi", type=("build", "run"))
    depends_on("mysql-client", type=("build", "link", "run"))
    conflicts("mariadb-c-client")
    conflicts("mariadb")

    def configure_args(self):
        mysql = self.spec["mysql-client"].prefix
        mysql_config = mysql.bin.mysql_config
        return [
            f"--cflags=-I{mysql.include}",
            f"--libs=-L{mysql.lib} -lmysqlclient",
            f"--mysql_config={mysql_config}",
        ]
