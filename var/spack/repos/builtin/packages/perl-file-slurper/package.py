# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlFileSlurper(PerlPackage):
    """A simple, sane and efficient module to slurp a file"""

    homepage = "http://search.cpan.org/~leont/File-Slurper/lib/File/Slurper.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/L/LE/LEONT/File-Slurper-0.011.tar.gz"

    version('0.011', 'e0482d3d5a0522e39132ba54af9f1ce3')
