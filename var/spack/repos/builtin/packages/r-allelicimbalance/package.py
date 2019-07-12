# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAllelicimbalance(RPackage):
    """Investigates Allele Specific Expression

       Provides a framework for allelic specific expression investigation using
       RNA-seq data."""

    homepage = "https://bioconductor.org/packages/AllelicImbalance"
    git      = "https://git.bioconductor.org/packages/AllelicImbalance.git"

    version('1.22.0', commit='04692e367e8c6aac475d06adfd7cfa629baab05a')
    version('1.20.0', commit='4cd3a789d872151b0d906ec419677271fecdf7c3')
    version('1.18.0', commit='6d6eed7487e9207dba556bc76283bcc7745808ea')
    version('1.16.0', commit='85f652ae8a0dd15535819b6e934065182df5544a')
    version('1.14.0', commit='35958534945819baafde0e13d1eb4d05a514142c')

    depends_on('r@3.6.0:3.6.9', when='@1.22.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.20.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.18.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.16.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.14.0', type=('build', 'run'))
