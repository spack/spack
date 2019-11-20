# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ROrganismdbi(RPackage):
    """The package enables a simple unified interface to several annotation
       packages each of which has its own schema by taking advantage of the
       fact that each of these packages implements a select methods."""

    homepage = "https://bioconductor.org/packages/OrganismDbi/"
    git      = "https://git.bioconductor.org/packages/OrganismDbi.git"

    version('1.18.1', commit='ba2d1237256805e935d9534a0c6f1ded07b42e95')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-genomicfeatures', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biocinstaller', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-rbgl', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.18.1')
