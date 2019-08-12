# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDigestMd5(PerlPackage):
    """Perl interface to the MD5 Algorithm"""

    homepage = "http://search.cpan.org/dist/Digest-MD5/MD5.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/Digest-MD5-2.55.tar.gz"

    version('2.55', '601519b826ca14c233f13a4578b967ef')
