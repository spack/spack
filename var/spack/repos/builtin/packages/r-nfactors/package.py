# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNfactors(RPackage):
    """nFactors: Parallel Analysis and Other Non Graphical Solutions to the
    Cattell Scree Test"""

    homepage = "https://cloud.r-project.org/package=nFactors"
    url      = "https://cloud.r-project.org/src/contrib/nFactors_2.4.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/nFactors"

    version('2.4.1',   sha256='028eb4ebd42a29f6a01297d728c7e353cabb37b46701639b4a52f17ba25a3eb6')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-psych', type=('build', 'run'))
