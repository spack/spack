# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlSubName(PerlPackage):
    """Name or rename a sub"""

    homepage = "http://search.cpan.org/~ether/Sub-Name-0.21/lib/Sub/Name.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Sub-Name-0.21.tar.gz"

    version('0.21', '7e7a181e30b3249d0b81585f55e36621')
