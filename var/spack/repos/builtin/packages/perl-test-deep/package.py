# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTestDeep(PerlPackage):
    """Extremely flexible deep comparison"""

    homepage = "http://search.cpan.org/~rjbs/Test-Deep-1.127/lib/Test/Deep.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Test-Deep-1.127.tar.gz"

    version('1.130', sha256='4064f494f5f62587d0ae501ca439105821ee5846c687dc6503233f55300a7c56')
    version('1.128', sha256='852d7e836fba8269b0b755082051a24a1a309d015a8b76838790af9e3760092f')
    version('1.127', sha256='b78cfc59c41ba91f47281e2c1d2bfc4b3b1b42bfb76b4378bc88cc37b7af7268')
