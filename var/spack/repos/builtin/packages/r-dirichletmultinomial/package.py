# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDirichletmultinomial(RPackage):
    """Dirichlet-multinomial mixture models can be used to describe
    variability in microbial metagenomic data.

    This package is an interface to code originally made available by
    Holmes, Harris, and Quince, 2012, PLoS ONE 7(2): 1-15, as discussed
    further in the man page for this package, ?DirichletMultinomial."""

    homepage = "https://bioconductor.org/packages/DirichletMultinomial/"
    git      = "https://git.bioconductor.org/packages/DirichletMultinomial.git"

    version('1.20.0', commit='251529f301da1482551142240aeb6baf8dab2272')

    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('gsl')
    depends_on('r@3.4.0:')
