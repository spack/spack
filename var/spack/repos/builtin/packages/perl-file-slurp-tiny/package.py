# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlFileSlurpTiny(PerlPackage):
    """A simple, sane and efficient file slurper"""

    homepage = "http://search.cpan.org/~leont/File-Slurp-Tiny-0.004/lib/File/Slurp/Tiny.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/L/LE/LEONT/File-Slurp-Tiny-0.004.tar.gz"

    version('0.004', '7575b81543281ea57cdb7e5eb3f73264')
