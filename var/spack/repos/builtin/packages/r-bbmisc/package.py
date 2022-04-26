# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBbmisc(RPackage):
    """Miscellaneous Helper Functions for B. Bischl.

    Miscellaneous helper functions for and from B. Bischl and some other guys,
    mainly for package development."""

    cran = "BBmisc"

    version('1.11', sha256='1ea48c281825349d8642a661bb447e23bfd651db3599bf72593bfebe17b101d2')

    depends_on('r-checkmate@1.8.0:', type=('build', 'run'))
