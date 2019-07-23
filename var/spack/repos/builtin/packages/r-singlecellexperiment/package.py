# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSinglecellexperiment(RPackage):
    """S4 Classes for Single Cell Data.

       Defines a S4 class for storing data from single-cell experiments. This
       includes specialized methods to store and retrieve spike-in information,
       dimensionality reduction coordinates and size factors for each cell,
       along with the usual metadata for genes and libraries."""

    homepage = "https://bioconductor.org/packages/SingleCellExperiment"
    git      = "https://git.bioconductor.org/packages/SingleCellExperiment.git"

    version('1.6.0', commit='baa51d77a8dacd2a22e7293095a8cffaaa3293b4')
    version('1.4.1', commit='b1efcb338e9176ae6829bb897957aa37e74d4870')
    version('1.2.0', commit='fe512259da79e0c660b322b5387e9bb16f2e6321')
    version('1.0.0', commit='545e974aa7ca7855e039bf9e3030290cd71d9031')

    depends_on('r@3.6.0:3.6.9', when='@1.6.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.4.1', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.2.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.0.0', type=('build', 'run'))

    depends_on('r-biocgenerics', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-s4vectors', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-summarizedexperiment', when='@1.0.0:', type=('build', 'run'))
