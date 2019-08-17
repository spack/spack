# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTryTiny(PerlPackage):
    """Minimal try/catch with proper preservation of $@"""

    homepage = "http://search.cpan.org/~ether/Try-Tiny-0.28/lib/Try/Tiny.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Try-Tiny-0.28.tar.gz"

    version('0.28', 'e2f8af601a62981aab30df15a6f47475')
