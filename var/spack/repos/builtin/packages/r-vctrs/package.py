# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVctrs(RPackage):
    """Vector Helpers.

    Defines new notions of prototype and size that are used to provide tools
    for consistent and well-founded type-coercion and size-recycling, and are
    in turn connected to ideas of type- and size-stability useful for analyzing
    function interfaces."""

    cran = "vctrs"

    version('0.3.8', sha256='7f4e8b75eda115e69dddf714f0643eb889ad61017cdc13af24389aab2a2d1bb1')
    version('0.3.6', sha256='df7d368c9f2d2ad14872ba2a09821ec4f5a8ad77c81a0b05e1f440e5ffebad25')
    version('0.3.5', sha256='11605d98106e294dae1a9b205462dd3906a6159a647150752b85dd290f6635cc')
    version('0.2.0', sha256='5bce8f228182ecaa51230d00ad8a018de9cf2579703e82244e0931fe31f20016')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r@3.3:', type=('build', 'run'), when='@0.3.5:')
    depends_on('r-ellipsis@0.2.0:', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-rlang@0.4.0:', type=('build', 'run'))
    depends_on('r-rlang@0.4.7:', type=('build', 'run'), when='@0.3.5:')
    depends_on('r-rlang@0.4.10:', type=('build', 'run'), when='@0.3.7:')

    depends_on('r-digest', type=('build', 'run'), when='@:0.3.6')
    depends_on('r-zeallot', type=('build', 'run'), when='@:0.2.0')
