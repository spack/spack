# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDataOptlist(PerlPackage):
    """Parse and validate simple name/value option pairs"""

    homepage = "http://search.cpan.org/~rjbs/Data-OptList-0.110/lib/Data/OptList.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Data-OptList-0.110.tar.gz"

    version('0.110', 'f9236c9ea5607134ad8a2b3dc901c4c5')

    depends_on('perl-sub-install', type=('build', 'run'))
