# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlPadwalker(PerlPackage):
    """play with other peoples' lexical variables"""

    homepage = "http://search.cpan.org/~robin/PadWalker-2.2/PadWalker.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RO/ROBIN/PadWalker-2.2.tar.gz"

    version('2.2', '6bcc741f77b1831a893b2a22c785e31a')
