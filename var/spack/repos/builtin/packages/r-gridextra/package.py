# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGridextra(RPackage):
    """Provides a number of user-level functions to work with "grid" graphics,
    notably to arrange multiple grid-based plots on a page, and draw tables."""

    homepage = "https://cloud.r-project.org/package=gridExtra"
    url      = "https://cloud.r-project.org/src/contrib/gridExtra_2.2.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gridExtras"

    version('2.3', '01e0ea88610756a0fd3b260e83c9bd43')
    version('2.2.1', '7076c2122d387c7ef3add69a1c4fc1b2')

    depends_on('r-gtable', type=('build', 'run'))
