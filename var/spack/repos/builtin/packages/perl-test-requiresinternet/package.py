# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTestRequiresinternet(PerlPackage):
    """Easily test network connectivity"""

    homepage = "http://search.cpan.org/~mallen/Test-RequiresInternet-0.05/lib/Test/RequiresInternet.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/M/MA/MALLEN/Test-RequiresInternet-0.05.tar.gz"

    version('0.05', '0ba9f1cff4cf90ed2618c2eddfd525d8')
