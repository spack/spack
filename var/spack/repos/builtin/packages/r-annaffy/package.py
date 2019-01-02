# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
#
from spack import *


class RAnnaffy(RPackage):
    """Functions for handling data from Bioconductor Affymetrix
    annotation data packages. Produces compact HTML and text
    reports including experimental data and URL links to many
    online databases. Allows searching biological metadata
    using various criteria."""

    homepage = "https://www.bioconductor.org/packages/annaffy/"
    git      = "https://git.bioconductor.org/packages/annaffy.git"

    version('1.48.0', commit='89a03c64ac9df5d963ed60b87893a3fffa6798a0')

    depends_on('r@3.4.0:3.4.9', when='@1.48.0')
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-go-db', type=('build', 'run'))
    depends_on('r-kegg-db', type=('build', 'run'))
