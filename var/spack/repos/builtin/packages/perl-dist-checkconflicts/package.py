# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDistCheckconflicts(PerlPackage):
    """Declare version conflicts for your dist"""

    homepage = "http://search.cpan.org/~doy/Dist-CheckConflicts-0.11/lib/Dist/CheckConflicts.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Dist-CheckConflicts-0.11.tar.gz"

    version('0.11', 'c8725a92b9169708b0f63036812070f2')
