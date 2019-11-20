# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSimpleaffy(RPackage):
    """Provides high level functions for reading Affy .CEL files,
       phenotypic data, and then computing simple things with it, such as
       t-tests, fold changes and the like. Makes heavy use of the affy
       library. Also has some basic scatter plot functions and mechanisms
       for generating high resolution journal figures..."""

    homepage = "http://bioconductor.org/packages/simpleaffy/"
    git      = "https://git.bioconductor.org/packages/simpleaffy.git"

    version('2.52.0', commit='f2b43fb9b8e6fa4c03fe28b4efb3144a0a42a385')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-gcrma', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.52.0')
