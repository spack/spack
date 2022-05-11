# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PerlTestException(PerlPackage):
    """Test exception-based code"""

    homepage = "https://metacpan.org/pod/Test::Exception"
    url      = "http://search.cpan.org/CPAN/authors/id/E/EX/EXODIST/Test-Exception-0.43.tar.gz"

    version('0.43', sha256='156b13f07764f766d8b45a43728f2439af81a3512625438deab783b7883eb533')

    depends_on('perl-sub-uplevel', type=('build', 'run'))
