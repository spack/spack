# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSpem(RPackage):
    """This package can optimize the parameter in S-system models given time
    series data"""

    homepage = "https://bioconductor.org/packages/SPEM/"
    git      = "https://git.bioconductor.org/packages/SPEM.git"

    version('1.18.0', commit='3ab425dd9889885eac328d26b73366a875cd250b')

    depends_on('r-rsolnp', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r@3.4.3:3.4.9', when='@1.18.0')
