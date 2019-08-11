# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCrosstalk(RPackage):
    """Provides building blocks for allowing HTML widgets to communicate with
    each other, with Shiny or without (i.e. static .html files)."""

    homepage = "https://cloud.r-project.org/package=crosstalk"
    url      = "https://cloud.r-project.org/src/contrib/crosstalk_1.0.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/crosstalk"

    version('1.0.0', 'c13c21b81af2154be3f08870fd3a7077')

    depends_on('r-htmltools@0.3.5:', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-shiny@0.11:', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
