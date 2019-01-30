# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlIoSessiondata(PerlPackage):
    """A wrapper around a single IO::Socket object"""

    homepage = "http://search.cpan.org/~phred/IO-SessionData-1.03/"
    url      = "http://search.cpan.org/CPAN/authors/id/P/PH/PHRED/IO-SessionData-1.03.tar.gz"

    version('1.03', '790f9e05465c774cf9a6299500463104')
