# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlLwpMediatypes(PerlPackage):
    """Guess media type for a file or a URL"""

    homepage = "https://metacpan.org/pod/LWP::MediaTypes"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/LWP-MediaTypes-6.02.tar.gz"

    version('6.02', sha256='18790b0cc5f0a51468495c3847b16738f785a2d460403595001e0b932e5db676')
