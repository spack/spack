# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGostats(RPackage):
    """A set of tools for interacting with GO and microarray data.
    A variety of basic manipulation tools for graphs, hypothesis
    testing and other simple calculations."""

    homepage = "https://www.bioconductor.org/packages/GOstats/"
    git      = "https://git.bioconductor.org/packages/GOstats.git"

    version('2.42.0', commit='8b29709064a3b66cf1d963b2be0c996fb48c873e')

    depends_on('r@3.4.1:3.4.9', when='@2.42.0')
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-category', type=('build', 'run'))
    depends_on('r-go-db', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-rbgl', type=('build', 'run'))
    depends_on('r-annotate', type=('build', 'run'))
    depends_on('r-annotationforge', type=('build', 'run'))
