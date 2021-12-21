# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlGraphReadwrite(PerlPackage):
    """Write out directed graph in Dot format"""

    homepage = "https://metacpan.org/pod/Graph::ReadWrite"
    url      = "http://search.cpan.org/CPAN/authors/id/N/NE/NEILB/Graph-ReadWrite-2.09.tar.gz"

    version('2.09', sha256='b01ef06ce922eea12d5ce614d63ddc5f3ee7ad0d05f9577051d3f87a89799a4a')
