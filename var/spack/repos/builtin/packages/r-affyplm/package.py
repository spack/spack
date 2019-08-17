# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAffyplm(RPackage):
    """A package that extends and improves the functionality of
    the base affy package. Routines that make heavy use of compiled
    code for speed. Central focus is on implementation of methods
    for fitting probe-level models and tools using these models.
    PLM based quality assessment tools."""

    homepage = "https://www.bioconductor.org/packages/affyPLM/"
    git      = "https://git.bioconductor.org/packages/affyPLM.git"

    version('1.52.1', commit='e8613a6018c4ee58045df6bf19128844f50a1f43')

    depends_on('r@3.4.0:3.4.9', when='@1.52.1')
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-gcrma', type=('build', 'run'))
    depends_on('r-preprocesscore', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
