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


class RSiggenes(RPackage):
    """Identification of differentially expressed genes and estimation of the
       False Discovery Rate (FDR) using both the Significance Analysis of
       Microarrays (SAM) and the Empirical Bayes Analyses of Microarrays
       (EBAM)."""

    homepage = "http://bioconductor.org/packages/siggenes/"
    git      = "https://git.bioconductor.org/packages/siggenes.git"

    version('1.50.0', commit='b1818f26e1449005ffd971df6bda8da0303080bc')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-multtest', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.50.0')
