# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPlotmo(RPackage):
    """Plot a Model's Residuals, Response, and Partial Dependence Plots.

    Plot model surfaces for a wide variety of models using partial dependence
    plots and other techniques. Also plot model residuals and other information
    on the model."""

    cran = "plotmo"

    version('3.6.1', sha256='245a0c87f0cca08746c6fdc60da2e3856cd69b1a2b7b5641293c620d4ae04343')
    version('3.6.0', sha256='c05afcc442f9542868beea5c3c40fb93b049f9b61c42725b2a1e2bc750c241e3')
    version('3.5.6', sha256='78f08dc897136d21fa8ade2acb6290351b569d29eb0592c7074c0be3cf2aa594')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-formula@1.2-3:', type=('build', 'run'))
    depends_on('r-plotrix', type=('build', 'run'))
    depends_on('r-teachingdemos', type=('build', 'run'))
