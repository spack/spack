# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlInlineC(PerlPackage):
    """C Language Support for Inline"""

    homepage = "http://search.cpan.org/~tinita/Inline-C-0.78/lib/Inline/C.pod"
    url      = "http://search.cpan.org/CPAN/authors/id/T/TI/TINITA/Inline-C-0.78.tar.gz"

    version('0.78', '710a454b5337b1cbf3f2ae5c8c45b413')

    depends_on('perl-yaml-libyaml', type=('build', 'run'))
    depends_on('perl-parse-recdescent', type=('build', 'run'))
    depends_on('perl-inline', type=('build', 'run'))
    depends_on('perl-pegex', type=('build', 'run'))
    depends_on('perl-file-copy-recursive', type=('build', 'run'))
