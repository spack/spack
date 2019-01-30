# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlModuleImplementation(PerlPackage):
    """Loads one of several alternate underlying implementations for a
    module"""

    homepage = "http://search.cpan.org/~drolsky/Module-Implementation/lib/Module/Implementation.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Module-Implementation-0.09.tar.gz"

    version('0.09', '52e3fe0ca6b1eff0488d59b7aacc0667')

    depends_on('perl-module-runtime', type=('build', 'run'))
    depends_on('perl-test-fatal', type=('build', 'run'))
    depends_on('perl-test-requires', type=('build', 'run'))
    depends_on('perl-try-tiny', type=('build', 'run'))
