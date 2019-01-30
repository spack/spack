# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPicante(RPackage):
    """R tools for integrating phylogenies and ecology"""

    homepage = "https://cran.r-project.org/package=picante"
    url      = "https://cran.r-project.org/src/contrib/picante_1.6-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/picante"

    version('1.6-2', 'e3eba6ef254068d2cfa9e96760bcd7a3')
    version('1.6-1', '73d86b90eceda582654e995d47236d6e')

    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-vegan', type=('build', 'run'))
