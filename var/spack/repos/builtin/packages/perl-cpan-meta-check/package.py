# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlCpanMetaCheck(PerlPackage):
    """This module verifies if requirements described in a CPAN::Meta object
       are present.."""

    homepage = "http://search.cpan.org/~leont/CPAN-Meta-Check-0.014/lib/CPAN/Meta/Check.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/L/LE/LEONT/CPAN-Meta-Check-0.014.tar.gz"

    version('0.014', 'ccd4448a7b08e1e3ef6f475030b282c9')

    depends_on('perl-test-deep', type=('build', 'run'))
