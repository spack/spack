# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSpeedglm(RPackage):
    """Fitting linear models and generalized linear models to
    large data sets by updating algorithms."""

    homepage = "https://cloud.r-project.org/package=speedglm"
    url      = "https://cloud.r-project.org/src/contrib/speedglm_0.3-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/speedglm"

    version('0.3-2', 'c4874d4c2a677d657a335186ebb63131')

    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
