# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAnnotationdbi(RPackage):
    """Provides user interface and database connection code for
    annotation data packages using SQLite data storage."""

    homepage = "https://www.bioconductor.org/packages/AnnotationDbi/"
    git      = "https://git.bioconductor.org/packages/AnnotationDbi.git"

    version('1.42.1', commit='71085b47ea2e1ef929bebe8b17eb8e8a573f98e3')
    version('1.38.2', commit='67d46facba8c15fa5f0eb47c4e39b53dbdc67c36')

    depends_on('r@3.4.0:3.4.9', when='@1.38.2', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.42.1', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-rsqlite', type=('build', 'run'))
