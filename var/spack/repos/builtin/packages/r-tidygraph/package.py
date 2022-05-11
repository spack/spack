# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RTidygraph(RPackage):
    """A Tidy API for Graph Manipulation.

    A graph, while not "tidy" in itself, can be thought of as two tidy data
    frames describing node and edge data respectively. 'tidygraph' provides an
    approach to manipulate these two virtual data frames using the API defined
    in the 'dplyr' package, as well as provides tidy interfaces to a lot of
    common graph algorithms."""

    cran = "tidygraph"

    version('1.2.0', sha256='057d6c42fc0144109f3ace7f5058cca7b2fe493c761daa991448b23f86b6129f')
    version('1.1.2', sha256='5642001d4cccb122d66481b7c61a06c724c02007cbd356ee61cb29726a56fafe')

    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-dplyr@0.8:', type=('build', 'run'))
    depends_on('r-dplyr@0.8.5:', type=('build', 'run'), when='@1.2.0:')
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-pillar', type=('build', 'run'))
