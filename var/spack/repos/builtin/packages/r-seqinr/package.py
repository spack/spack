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


class RSeqinr(RPackage):
    """Exploratory data analysis and data visualization for biological
    sequence (DNA and protein) data. Includes also utilities for sequence
    data management under the ACNUC system."""

    homepage = "http://seqinr.r-forge.r-project.org"
    url      = "https://cran.r-project.org/src/contrib/seqinr_3.3-6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/seginr"

    version('3.4-5', 'd550525dcea754bbd5b83cb46b4124cc')
    version('3.3-6', '73023d627e72021b723245665e1ad055')

    depends_on('r@2.10:')
    depends_on('r-ade4', type=('build', 'run'))
    depends_on('r-segmented', type=('build', 'run'))
    depends_on('zlib')
