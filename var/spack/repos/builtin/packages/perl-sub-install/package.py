# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlSubInstall(PerlPackage):
    """Install subroutines into packages easily"""

    homepage = "http://search.cpan.org/~rjbs/Sub-Install-0.928/lib/Sub/Install.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Sub-Install-0.928.tar.gz"

    version('0.928', 'e1ce4f9cb6b2f6b8778b036c31afa5ab')
