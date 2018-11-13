# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlWant(PerlPackage):
    """A generalisation of wantarray."""

    homepage = "search.cpan.org/~robin/Want/Want.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RO/ROBIN/Want-0.29.tar.gz"

    version('0.29', '33b2dae5db59781b9a0434fa1db04aab')
