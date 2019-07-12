# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAnalysispageserver(RPackage):
    """A framework for sharing interactive data and plots from R through the
       web

       AnalysisPageServer is a modular system that enables sharing of
       customizable R analyses via the web."""

    homepage = "https://bioconductor.org/packages/AnalysisPageServer"
    git      = "https://git.bioconductor.org/packages/AnalysisPageServer.git"

    version('1.18.0', commit='655987c2787def419fcc2aa0fbf665ba0fd91f3b')
    version('1.16.0', commit='67b063523f80e2af1d26262367ff50f34e195174')
    version('1.14.0', commit='620c0ea1e129ddd1a0866e2c9d7c3fcf06a8baf4')
    version('1.12.0', commit='146501974ef1938ee1ec4eb293ea7eeca331a0dc')
    version('1.10.0', commit='876c87073be116fa15a1afdd407e21152eb80d50')

    depends_on('r@3.6.0:3.6.9', when='@1.18.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.16.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.14.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.12.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.10.0', type=('build', 'run'))
