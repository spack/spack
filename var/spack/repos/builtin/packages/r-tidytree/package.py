# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RTidytree(RPackage):
    """A Tidy Tool for Phylogenetic Tree Data Manipulation.

    Phylogenetic tree generally contains multiple components including node,
    edge, branch and associated data. 'tidytree' provides an approach to
    convert tree object to tidy data frame as well as provides tidy interfaces
    to manipulate tree data."""

    cran = "tidytree"

    version('0.3.7', sha256='7816f2d48ec94ca0c1bef15ec3d536adf44a969ea3c3cfc203ceebe16808e4f2')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-tidyselect', type=('build', 'run'))
    depends_on('r-yulab-utils@0.0.4:', type=('build', 'run'))
