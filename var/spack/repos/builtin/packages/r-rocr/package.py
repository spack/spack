# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
