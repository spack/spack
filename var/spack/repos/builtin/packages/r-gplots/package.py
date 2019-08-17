# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
#
from spack import *


class RGplots(RPackage):
    """Various R Programming Tools for Plotting Data."""

    homepage = "https://cloud.r-project.org/package=gplots"
    url      = "https://cloud.r-project.org/src/contrib/gplots_3.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gplots"

    version('3.0.1.1', sha256='7db103f903a25d174cddcdfc7b946039b61e236c95084b90ad17f1a41da3770c')
    version('3.0.1', '6116822401d55add044beb120ca93d14')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-gtools', type=('build', 'run'))
    depends_on('r-gdata', type=('build', 'run'))
    depends_on('r-catools', type=('build', 'run'))
    depends_on('r-kernsmooth', type=('build', 'run'))
