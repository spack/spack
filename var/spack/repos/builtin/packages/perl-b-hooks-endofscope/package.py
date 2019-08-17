# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlBHooksEndofscope(PerlPackage):
    """Execute code after a scope finished compilation."""

    homepage = "http://search.cpan.org/~ether/B-Hooks-EndOfScope-0.21/lib/B/Hooks/EndOfScope.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/B-Hooks-EndOfScope-0.21.tar.gz"

    version('0.21', 'df9dacbf55a01d7a444b1ebc616435ae')

    depends_on('perl-sub-exporter-progressive', type=('build', 'run'))
