# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RVsn(RPackage):
    """The package implements a method for normalising microarray intensities,
       and works for single- and multiple-color arrays. It can also be used
       for data from other technologies, as long as they have similar format.
       The method uses a robust variant of the maximum-likelihood estimator
       for an additive-multiplicative error model and affine calibration. The
       model incorporates data calibration step (a.k.a. normalization), a
       model for the dependence of the variance on the mean intensity and a
       variance stabilizing data transformation. Differences between
       transformed intensities are analogous to "normalized log-ratios".
       However, in contrast to the latter, their variance is independent of
       the mean, and they are usually more sensitive and specific in detecting
       differential transcription."""

    homepage = "https://www.bioconductor.org/packages/vsn/"
    git      = "https://git.bioconductor.org/packages/vsn.git"

    version('3.44.0', commit='e54513fcdd07ccfb8094359e93cef145450f0ee0')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-hexbin', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@3.44.0')
