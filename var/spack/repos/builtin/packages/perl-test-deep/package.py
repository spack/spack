# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTestDeep(PerlPackage):
    """Extremely flexible deep comparison"""

    homepage = "https://metacpan.org/pod/Test::Deep"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Test-Deep-1.127.tar.gz"

    version('1.127', sha256='b78cfc59c41ba91f47281e2c1d2bfc4b3b1b42bfb76b4378bc88cc37b7af7268')
