# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBbmisc(RPackage):
    """Miscellaneous helper functions for and from B. Bischl and some other
       guys, mainly for package development."""

    homepage = "https://github.com/berndbischl/BBmisc"
    url      = "https://cloud.r-project.org/src/contrib/BBmisc_1.11.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/BBmisc"

    version('1.11', '681642628037406beb6088d5f773473d')

    depends_on('r-checkmate@1.8.0:', type=('build', 'run'))
