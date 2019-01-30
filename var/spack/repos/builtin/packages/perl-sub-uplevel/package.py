# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlSubUplevel(PerlPackage):
    """apparently run a function in a higher stack frame"""

    homepage = "http://search.cpan.org/~dagolden/Sub-Uplevel-0.2800/lib/Sub/Uplevel.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/Sub-Uplevel-0.2800.tar.gz"

    version('0.2800', '6c6a174861fd160e8d5871a86df00baf')
