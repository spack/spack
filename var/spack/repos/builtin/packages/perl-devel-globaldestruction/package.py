# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDevelGlobaldestruction(PerlPackage):
    """Makes Perl's global destruction less tricky to deal with"""

    homepage = "http://search.cpan.org/~haarg/Devel-GlobalDestruction-0.14/lib/Devel/GlobalDestruction.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/H/HA/HAARG/Devel-GlobalDestruction-0.14.tar.gz"

    version('0.14', '24221ba322cf2dc46a1fc99b53e2380b')
