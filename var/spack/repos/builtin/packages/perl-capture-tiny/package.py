# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlCaptureTiny(PerlPackage):
    """Capture STDOUT and STDERR from Perl, XS or external programs"""

    homepage = "http://search.cpan.org/~dagolden/Capture-Tiny-0.46/lib/Capture/Tiny.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/Capture-Tiny-0.46.tar.gz"

    version('0.46', 'd718af07729d26a793949ca6ba2580a7')
