# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PerlPackageStashXs(PerlPackage):
    """Faster and more correct implementation of the Package::Stash API"""

    homepage = "https://metacpan.org/pod/Package::Stash::XS"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Package-Stash-XS-0.28.tar.gz"

    version('0.28', sha256='23d8c5c25768ef1dc0ce53b975796762df0d6e244445d06e48d794886c32d486')
