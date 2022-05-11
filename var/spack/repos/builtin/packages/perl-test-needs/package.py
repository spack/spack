# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestNeeds(PerlPackage):
    """Skip tests when modules not available."""

    homepage = "https://metacpan.org/pod/Test::Needs"
    url      = "https://search.cpan.org/CPAN/authors/id/H/HA/HAARG/Test-Needs-0.002005.tar.gz"

    version('0.002005', sha256='5a4f33983586edacdbe00a3b429a9834190140190dab28d0f873c394eb7df399')
