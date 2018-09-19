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


class RRocr(RPackage):
    """ROC graphs, sensitivity/specificity curves, lift charts,
    and precision/recall plots are popular examples of trade-off
    visualizations for specific pairs of performance measures. ROCR
    is a flexible tool for creating cutoff-parameterized 2D performance
    curves by freely combining two from over 25 performance measures
    (new performance measures can be added using a standard interface).
    Curves from different cross-validation or bootstrapping runs can
    be averaged by different methods, and standard deviations, standard
    errors or box plots can be used to visualize the variability across
    the runs. The parameterization can be visualized by printing cutoff
    values at the corresponding curve positions, or by coloring the
    curve according to cutoff. All components of a performance plot
    can be quickly adjusted using a flexible parameter dispatching
    mechanism. Despite its flexibility, ROCR is easy to use, with only
    three commands and reasonable default values for all optional
    parameters."""
    homepage = "https://cran.r-project.org/package=ROCR"
    url      = "https://cran.rstudio.com/src/contrib/ROCR_1.0-7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ROCR"

    version('1.0-7', '46cbd43ae87fc4e1eff2109529a4820e')
    depends_on('r-gplots', type=('build', 'run'))
