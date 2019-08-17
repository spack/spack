# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTaskWeaken(PerlPackage):
    """Ensure that a platform has weaken support"""

    homepage = "http://search.cpan.org/~adamk/Task-Weaken-1.04/lib/Task/Weaken.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Task-Weaken-1.04.tar.gz"

    version('1.04', 'affd0c395515bb95d29968404d7fe6de')
