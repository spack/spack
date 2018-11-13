# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlCompressRawBzip2(PerlPackage):
    """A low-Level Interface to bzip2 compression library."""

    homepage = "http://search.cpan.org/~pmqs/Compress-Raw-Bzip2-2.081/lib/Compress/Raw/Bzip2.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/Compress-Raw-Bzip2-2.081.tar.gz"

    version('2.081', '25fa9c9cc4fd3250b65b91694f9eac2e')

    depends_on('bzip2')
    depends_on('perl-extutils-makemaker', type='build')
