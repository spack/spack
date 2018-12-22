# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RA4(RPackage):
    """Automated Affymetrix Array Analysis Umbrella Package."""

    homepage = "https://www.bioconductor.org/packages/a4/"
    git      = "https://git.bioconductor.org/packages/a4.git"

    version('1.24.0', commit='79b5143652176787c85a0d587b3bbfad6b4a19f4')

    depends_on('r@3.4.0:3.4.9', when='@1.24.0')
    depends_on('r-a4base', type=('build', 'run'))
    depends_on('r-a4preproc', type=('build', 'run'))
    depends_on('r-a4classif', type=('build', 'run'))
    depends_on('r-a4core', type=('build', 'run'))
    depends_on('r-a4reporting', type=('build', 'run'))
