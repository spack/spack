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


class RMaldiquant(RPackage):
    """A complete analysis pipeline for matrix-assisted laser
       desorption/ionization-time-of-flight (MALDI-TOF) and other
       two-dimensional mass spectrometry data. In addition to commonly used
       plotting and processing methods it includes distinctive features,
       namely baseline subtraction methods such as morphological filters
       (TopHat) or the statistics-sensitive non-linear iterative peak-clipping
       algorithm (SNIP), peak alignment using warping functions, handling of
       replicated measurements as well as allowing spectra with different
       resolutions."""

    homepage = "https://cran.r-project.org/package=MALDIquant"
    url      = "https://cran.r-project.org/src/contrib/MALDIquant_1.16.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/MALDIquant"

    version('1.16.4', '83200e7496d05c5a99292e45d2b11c67')

    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-testthat', type=('build', 'run'))
