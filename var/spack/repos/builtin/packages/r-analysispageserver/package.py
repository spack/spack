# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAnalysispageserver(RPackage):
    """AnalysisPageServer is a modular system that enables sharing
    of customizable R analyses via the web."""

    homepage = "https://www.bioconductor.org/packages/AnalysisPageServer/"
    git      = "https://git.bioconductor.org/packages/AnalysisPageServer.git"

    version('1.10.0', commit='876c87073be116fa15a1afdd407e21152eb80d50')

    depends_on('r@3.4.0:3.4.9', when='@1.10.0')
    depends_on('r-log4r', type=('build', 'run'))
    depends_on('r-rjson', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
