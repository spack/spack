# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlNamespaceClean(PerlPackage):
    """Keep imports and functions out of your namespace."""

    homepage = "http://search.cpan.org/~ribasushi/namespace-clean-0.27/lib/namespace/clean.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RI/RIBASUSHI/namespace-clean-0.27.tar.gz"

    version('0.27', 'cba97f39ef7e594bd8489b4fdcddb662')

    depends_on('perl-b-hooks-endofscope', type=('build', 'run'))
