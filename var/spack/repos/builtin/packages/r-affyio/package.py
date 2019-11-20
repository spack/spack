# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAffyio(RPackage):
    """Routines for parsing Affymetrix data files based upon file format
       information. Primary focus is on accessing the CEL and CDF file
       formats."""

    homepage = "https://bioconductor.org/packages/affyio/"
    git      = "https://git.bioconductor.org/packages/affyio.git"

    version('1.46.0', commit='977597f2772e08273d86579486f452170566c880')

    depends_on('r-zlibbioc', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.46.0')
