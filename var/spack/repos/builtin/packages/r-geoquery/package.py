# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGeoquery(RPackage):
    """The NCBI Gene Expression Omnibus (GEO) is a public repository of
       microarray data. Given the rich and varied nature of this resource,
       it is only natural to want to apply BioConductor tools to these data.
       GEOquery is the bridge between GEO and BioConductor."""

    homepage = "https://bioconductor.org/packages/GEOquery/"
    git      = "https://git.bioconductor.org/packages/GEOquery.git"

    version('2.42.0', commit='c26adef8d3ddbd6932a3170f2f84f6e4327641fb')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-rcurl', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.42.0')
