# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlPerlioGzip(PerlPackage):
    """Perl extension to provide a PerlIO layer to gzip/gunzip"""

    homepage = "http://search.cpan.org/~nwclark/PerlIO-gzip/gzip.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/N/NW/NWCLARK/PerlIO-gzip-0.19.tar.gz"

    version('0.20', '0393eae5d0b23df6cf40ed44af7d711c')
    version('0.19', 'dbcfc1450f6b593b65048b8ced061c98')
