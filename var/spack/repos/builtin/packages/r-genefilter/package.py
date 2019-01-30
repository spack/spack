# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGenefilter(RPackage):
    """Some basic functions for filtering genes"""

    homepage = "https://bioconductor.org/packages/genefilter/"
    git      = "https://git.bioconductor.org/packages/genefilter.git"

    version('1.62.0', commit='eb119894f015c759f93f458af7733bdb770a22ad')
    version('1.58.1', commit='ace2556049677f60882adfe91f8cc96791556fc2')

    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-annotate', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.58.1', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.62.0', type=('build', 'run'))
