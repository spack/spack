# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLabelled(RPackage):
    """Work with labelled data imported from 'SPSS' or 'Stata' with 'haven' or
    'foreign'. This package provides useful functions to deal with
    "haven_labelled" and "haven_labelled_spss" classes introduced by 'haven'
    package."""

    homepage = "https://cloud.r-project.org/package=labelled"
    url      = "https://cloud.r-project.org/src/contrib/labelled_2.7.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/labelled"

    version('2.7.0', sha256='b1b66b34d3ad682e492fc5bb6431780760576d29dbac40d87bef3c0960054bdb')

    depends_on('r-haven@2.3.1:', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-lifecycle', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-vctrs', type=('build', 'run'))
    depends_on('r-pillar', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
