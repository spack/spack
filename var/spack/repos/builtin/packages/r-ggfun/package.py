# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGgfun(RPackage):
    """Miscellaneous Functions for 'ggplot2'.

    Useful functions to edit 'ggplot' object (e.g., setting fonts for theme and
    layers, adding rounded rectangle as background for each of the legends)."""

    cran = "ggfun"

    version('0.0.5', sha256='b1e340a8932d2cffbbbf6070ce96c9356599e9955a2b6534fcb17e599c575783')
    version('0.0.4', sha256='5926365f9a90baf47320baf48c40f515ef570f9c767484adea5f04219964d21e')

    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
