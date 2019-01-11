# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDbdMysql(PerlPackage):
    """MySQL driver for the Perl5 Database Interface (DBI)"""

    homepage = "http://search.cpan.org/~michielb/DBD-mysql-4.043/lib/DBD/mysql.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/M/MI/MICHIELB/DBD-mysql-4.043.tar.gz"

    version('4.043', '4a00dd7f1c057931147c65dfc4901c36')

    depends_on('perl-test-deep', type=('build', 'run'))
    depends_on('perl-dbi', type=('build', 'run'))
    depends_on('mariadb@:10.1.23')
