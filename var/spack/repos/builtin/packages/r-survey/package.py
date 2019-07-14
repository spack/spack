# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSurvey(RPackage):
    """Summary statistics, two-sample tests, rank tests, generalised linear
    models, cumulative link models, Cox models, loglinear models, and general
    maximum pseudolikelihood estimation for multistage stratified,
    cluster-sampled, unequally weighted survey samples. Variances by Taylor
    series linearisation or replicate weights. Post-stratification,
    calibration, and raking. Two-phase subsampling designs. Graphics. PPS
    sampling without replacement. Principal components, factor analysis."""

    homepage = "http://r-survey.r-forge.r-project.org/survey/"
    url      = "https://cran.r-project.org/src/contrib/survey_3.30-3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/survey"

    version('3.35-1', sha256='11e5ddde9c8c21dfaed0b1247036e068ad32782c76ff71f7937eb7585dd364db')
    version('3.30-3', 'c70cdae9cb43d35abddd11173d64cad0')
