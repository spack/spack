# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAnnotate(RPackage):
    """Using R enviroments for annotation."""

    homepage = "https://www.bioconductor.org/packages/annotate/"
    git      = "https://git.bioconductor.org/packages/annotate.git"

    version('1.58.0', commit='d1b5dd5feb8793f4f816d9a4aecbebb5ec7df7bc')
    version('1.54.0', commit='860cc5b696795a31b18beaf4869f9c418d74549e')

    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-rcurl', type=('build', 'run'))
    depends_on('r-xtable', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.54.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.58.0', type=('build', 'run'))
