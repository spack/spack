# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTimePiece(PerlPackage):
    """Object Oriented time objects"""

    homepage = "http://search.cpan.org/~esaym/Time-Piece/Piece.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ES/ESAYM/Time-Piece-1.3203.tar.gz"

    version('1.3203', '515c1306f123a00116a95335cf543501')
