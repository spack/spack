# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTestDeep(PerlPackage):
    """Extremely flexible deep comparison"""

    homepage = "http://search.cpan.org/~rjbs/Test-Deep-1.127/lib/Test/Deep.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Test-Deep-1.127.tar.gz"

    version('1.127', 'eeafe5795ba20ba051a1423f4fa86dd6')
