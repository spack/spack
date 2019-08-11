# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSamr(RPackage):
    """Significance Analysis of Microarrays."""

    homepage = "https://cloud.r-project.org/package=samr"
    url      = "https://cloud.r-project.org/src/contrib/samr_2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/samr"
    version('3.0', sha256='25f88ac002c2adce8881a562241bc12d683810a05defb553e8e3d4878f037506')
    version('2.0', 'e8f50b8b25069d03d42c2c61c72b0da0')

    depends_on('r-impute', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
    depends_on('r-shiny', when='@3.0:', type=('build', 'run'))
    depends_on('r-shinyfiles', when='@3.0:', type=('build', 'run'))
    depends_on('r-openxlsx', when='@3.0:', type=('build', 'run'))
    depends_on('r-gsa', when='@3.0:', type=('build', 'run'))
