# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RVctrs(RPackage):
    """Defines new notions of prototype and size that are used to provide tools
    for consistent and well-founded type-coercion and size-recycling, and are
    in turn connected to ideas of type- and size-stability useful for analyzing
    function interfaces."""

    homepage = "https://github.com/r-lib/vctrs"
    url      = "https://cloud.r-project.org/src/contrib/vctrs_0.2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/vctrs"

    version('0.2.0', sha256='5bce8f228182ecaa51230d00ad8a018de9cf2579703e82244e0931fe31f20016')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r-backports', type=('build', 'run'))
    depends_on('r-ellipsis@0.2.0:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-rlang@0.4.0:', type=('build', 'run'))
    depends_on('r-zeallot', type=('build', 'run'))
