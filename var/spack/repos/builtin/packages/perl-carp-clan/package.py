# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlCarpClan(PerlPackage):
    """Report errors from perspective of caller of a "clan" of modules"""

    homepage = "http://search.cpan.org/~kentnl/Carp-Clan-6.06/lib/Carp/Clan.pod"
    url      = "http://search.cpan.org/CPAN/authors/id/K/KE/KENTNL/Carp-Clan-6.06.tar.gz"

    version('6.06', 'c562a35c48f43665fab735cdc7fe3cb2')

    depends_on('perl-test-exception', type=('build', 'run'))
    depends_on('perl-sub-uplevel', type=('build', 'run'))
