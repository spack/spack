# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTestNeeds(PerlPackage):
    """Skip tests when modules not available."""

    homepage = "http://search.cpan.org/~haarg/Test-Needs-0.002005/lib/Test/Needs.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/H/HA/HAARG/Test-Needs-0.002005.tar.gz"

    version('0.002005', '356634a56c99282e8059f290f5d534c8')
