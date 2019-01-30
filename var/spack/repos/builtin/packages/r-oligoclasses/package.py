# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ROligoclasses(RPackage):
    """This package contains class definitions, validity checks,
    and initialization methods for classes used by the oligo and
    crlmm packages."""

    homepage = "https://www.bioconductor.org/packages/oligoClasses/"
    git      = "https://git.bioconductor.org/packages/oligoClasses.git"

    version('1.38.0', commit='fe2bb7f02c7ed3cbd338254c27ceba6ff829a962')

    depends_on('r@3.4.0:3.4.9', when='@1.38.0')
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-summarizedexperiment', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-affyio', type=('build', 'run'))
    depends_on('r-ff', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-biocinstaller', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-rsqlite', type=('build', 'run'))
