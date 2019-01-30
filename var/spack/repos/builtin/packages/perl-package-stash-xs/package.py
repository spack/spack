# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlPackageStashXs(PerlPackage):
    """Faster and more correct implementation of the Package::Stash API"""

    homepage = "http://search.cpan.org/~doy/Package-Stash-XS-0.28/lib/Package/Stash/XS.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Package-Stash-XS-0.28.tar.gz"

    version('0.28', '9664356ec3be02626cbd3081ec246b70')
