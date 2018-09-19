##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
