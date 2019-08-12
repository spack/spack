# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlSvg(PerlPackage):
    """Perl extension for generating Scalable Vector Graphics (SVG) documents.
    """

    homepage = "http://search.cpan.org/~manwar/SVG-2.78/lib/SVG.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/M/MA/MANWAR/SVG-2.78.tar.gz"

    version('2.78', 'b247c216ab11fae24533d0ce556e2e75')
