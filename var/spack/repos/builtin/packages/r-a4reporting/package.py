# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RA4reporting(RPackage):
    """Automated Affymetrix Array Analysis Reporting Package."""

    homepage = "https://www.bioconductor.org/packages/a4Reporting"
    git      = "https://git.bioconductor.org/packages/a4Reporting.git"

    version('1.24.0', commit='bf22c4d50daf40fc9eaf8c476385bf4a24a5b5ce')

    depends_on('r@3.4.0:3.4.9', when='@1.24.0')
    depends_on('r-annaffy', type=('build', 'run'))
    depends_on('r-xtable', type=('build', 'run'))
