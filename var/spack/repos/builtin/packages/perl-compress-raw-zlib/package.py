# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlCompressRawZlib(PerlPackage):
    "A low-Level Interface to zlib compression library"

    homepage = "http://search.cpan.org/~pmqs/Compress-Raw-Zlib-2.081/lib/Compress/Raw/Zlib.pm"
    url      = "https://cpan.metacpan.org/authors/id/P/PM/PMQS/Compress-Raw-Zlib-2.081.tar.gz"

    version('2.081', 'a22d23bb4f8ce92a41ace1dff29f2bd1')

    depends_on('zlib')
    depends_on('perl-extutils-makemaker', type='build')
