# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTextCsv(PerlPackage):
    """Comma-separated values manipulator (using XS or PurePerl)"""

    homepage = "http://search.cpan.org/~ishigaki/Text-CSV/lib/Text/CSV.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/I/IS/ISHIGAKI/Text-CSV-1.95.tar.gz"

    version('1.95', '1e076b4b1f8ba6a5003bf93f3c437a9e')
