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


class RProc(RPackage):
    """Tools for visualizing, smoothing and comparing receiver operating
       characteristic (ROC curves). (Partial) area under the curve (AUC)
       can be compared with statistical tests based on U-statistics or
       bootstrap. Confidence intervals can be computed for (p)AUC or
       ROC curves."""

    homepage = "https://web.expasy.org/pROC/"
    url      = "https://cran.r-project.org/src/contrib/pROC_1.12.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/pROC"

    version('1.12.1', 'ef5fb446fd75c1a3a5e7abf9b7aa4f75')

    depends_on('r@2.14:', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-rcpp@0.11.1:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
