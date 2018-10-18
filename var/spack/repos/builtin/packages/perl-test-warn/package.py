# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTestWarn(PerlPackage):
    """Perl extension to test methods for warnings"""

    homepage = "http://search.cpan.org/~chorny/Test-Warn-0.30/Warn.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/C/CH/CHORNY/Test-Warn-0.30.tar.gz"

    version('0.30', '8306b998a96d2cc69266b5248d550472')
