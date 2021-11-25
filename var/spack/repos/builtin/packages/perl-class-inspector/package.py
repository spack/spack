# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlClassInspector(PerlPackage):
    """Get information about a class and its structure"""

    homepage = "https://metacpan.org/pod/Class::Inspector"
    url      = "http://search.cpan.org/CPAN/authors/id/P/PL/PLICEASE/Class-Inspector-1.32.tar.gz"

    version('1.32', sha256='cefadc8b5338e43e570bc43f583e7c98d535c17b196bcf9084bb41d561cc0535')
