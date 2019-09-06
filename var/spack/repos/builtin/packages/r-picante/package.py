# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPicante(RPackage):
    """R tools for integrating phylogenies and ecology"""

    homepage = "https://cloud.r-project.org/package=picante"
    url      = "https://cloud.r-project.org/src/contrib/picante_1.6-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/picante"

    version('1.8', sha256='81a6308dbb53c9cdab30c1f9ac727abee76314351823b3a2142c21ed8e1498ad')
    version('1.7', sha256='75e4d73080db67e776562a1d58685438461cbde39af46900c7838da56aef0a62')
    version('1.6-2', 'e3eba6ef254068d2cfa9e96760bcd7a3')
    version('1.6-1', '73d86b90eceda582654e995d47236d6e')

    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-vegan', type=('build', 'run'))
