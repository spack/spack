# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMsnbase(RPackage):
    """Manipulation, processing and visualisation of mass spectrometry and
       proteomics data."""

    homepage = "https://www.bioconductor.org/packages/MSnbase/"
    git      = "https://git.bioconductor.org/packages/MSnbase.git"

    version('2.2.0', commit='d6e8fb7f106d05096fa9074da0f829ac8f02c197')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-mzr', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-protgenerics', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-preprocesscore', type=('build', 'run'))
    depends_on('r-vsn', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-impute', type=('build', 'run'))
    depends_on('r-pcamethods', type=('build', 'run'))
    depends_on('r-mzid', type=('build', 'run'))
    depends_on('r-maldiquant', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.2.0')
