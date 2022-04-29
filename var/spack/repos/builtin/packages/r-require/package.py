# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RRequire(RPackage):
    """Installing and Loading R Packages for Reproducible Workflows.

    A single key function, 'Require' that wraps 'install.packages',
    'remotes::install_github', 'versions::install.versions', and
    'base::require' that allows for reproducible workflows. As with other
    functions in a reproducible workflow, this package emphasizes functions
    that return the same result whether it is the first or subsequent times
    running the function. Maturing."""

    cran = "Require"

    maintainers = ['dorton21']

    version('0.0.13', sha256='ad9cb167694abe70beadc972c2c25086f0ac8e7e5802bf9606c1868e01be2526')
    version('0.0.10', sha256='2087c3bb4d660d205962e241c1fc4a366dada5a1ed090d545c52188490567f8d')

    depends_on('r@3.5:', type=('build', 'run'))
    depends_on('r@3.6:', type=('build', 'run'), when='@0.0.13:')
    depends_on('r-data-table@1.10.4:', type=('build', 'run'))
    depends_on('r-remotes', type=('build', 'run'))
