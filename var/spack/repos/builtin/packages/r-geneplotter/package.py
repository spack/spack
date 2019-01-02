# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGeneplotter(RPackage):
    """Functions for plotting genomic data."""

    homepage = "https://www.bioconductor.org/packages/geneplotter/"
    git      = "https://git.bioconductor.org/packages/geneplotter.git"

    version('1.58.0', commit='2b3f44804d61a40cfe7eaedf74ac9f5a054f7fde')
    version('1.54.0', commit='efdd946e092e44e35fde1eb4bcc5ec1d52090940')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-annotate', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.54.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.58.0', type=('build', 'run'))
