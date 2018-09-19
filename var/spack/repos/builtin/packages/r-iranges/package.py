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


class RIranges(RPackage):
    """Provides efficient low-level and highly
    reusable S4 classes for storing,
    manipulating and aggregating over annotated ranges of
    integers. Implements an
    algebra of range operations, including efficient
    algorithms for finding overlaps
    and nearest neighbors. Defines efficient list-like
    classes for storing, transforming
    and aggregating large grouped data,
    i.e., collections of atomic vectors and DataFrames."""

    homepage = "https://www.bioconductor.org/packages/IRanges/"
    git      = "https://git.bioconductor.org/packages/IRanges.git"

    version('2.14.10', commit='c76118a38e84c7c764141adbd66ee350d0882bc9')
    version('2.12.0', commit='1b1748655a8529ba87ad0f223f035ef0c08e7fcd')
    version('2.10.5', commit='b00d1d5025e3c480d17c13100f0da5a0132b1614')

    depends_on('r-biocgenerics@0.21.1:', type=('build', 'run'), when='@2.10.5')
    depends_on('r-biocgenerics@0.23.3:', type=('build', 'run'), when='@2.12.0')
    depends_on('r-biocgenerics@0.25.3:', type=('build', 'run'), when='@2.14.10')
    depends_on('r-s4vectors@0.13.17:', type=('build', 'run'), when='@2.10.5')
    depends_on('r-s4vectors@0.15.5:', type=('build', 'run'), when='@2.12.0')
    depends_on('r-s4vectors@0.18.2:', type=('build', 'run'), when='@2.14.10')
    depends_on('r@3.4.0:3.4.9', when='@2.10.5', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.14.10', type=('build', 'run'))
