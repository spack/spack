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
