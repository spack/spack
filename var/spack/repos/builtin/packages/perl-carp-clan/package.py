# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlCarpClan(PerlPackage):
    """Report errors from perspective of caller of a "clan" of modules"""

    homepage = "https://metacpan.org/pod/Carp::Clan"
    url      = "http://search.cpan.org/CPAN/authors/id/K/KE/KENTNL/Carp-Clan-6.06.tar.gz"

    version('6.06', sha256='ea4ac8f611354756d43cb369880032901e9cc4cc7e0bebb7b647186dac00c9d4')

    depends_on('perl-test-exception', type=('build', 'run'))
    depends_on('perl-sub-uplevel', type=('build', 'run'))
