# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlVersion(PerlPackage):
    """Parse and manipulate Perl version strings"""

    homepage = "http://search.cpan.org/~bdfoy/Perl-Version-1.013/lib/Perl/Version.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/B/BD/BDFOY/Perl-Version-1.013_03.tar.gz"

    version('1.013_03', 'b2c94c8b33ccfa1635c760fcfa1c5358')

    depends_on('perl-file-slurp-tiny', type=('build', 'run'))
