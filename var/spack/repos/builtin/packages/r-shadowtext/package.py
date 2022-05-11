# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RShadowtext(RPackage):
    """Shadow Text Grob and Layer.

    Implement shadowtextGrob() for 'grid' and geom_shadowtext() layer for
    'ggplot2'. These functions create/draw text grob with background shadow."""

    cran = "shadowtext"

    version('0.1.1', sha256='eb06581d7ed06c963eee47548932688fd48eba70b3ebd2a7b41a6501d6e00006')
    version('0.0.7', sha256='6e32b1dfd3d4816803848b876666185258b888286ec3d3e8500499ec3eba31e8')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
