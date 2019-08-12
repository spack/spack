# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlPdfApi2(PerlPackage):
    """Facilitates the creation and modification of PDF files"""

    homepage = "http://search.cpan.org/~ssimms/PDF-API2-2.033/lib/PDF/API2.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/S/SS/SSIMMS/PDF-API2-2.033.tar.gz"

    version('2.033', '4223a38add42741f996bd67d5f2f8e5b')

    depends_on('perl-test-exception', type=('build', 'run'))
    depends_on('perl-test-memory-cycle', type=('build', 'run'))
    depends_on('perl-font-ttf', type=('build', 'run'))
