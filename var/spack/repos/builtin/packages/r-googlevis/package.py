# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGooglevis(RPackage):
    """R interface to Google Charts API, allowing users to create interactive
    charts based on data frames. Charts are displayed locally via the R HTTP
    help server. A modern browser with an Internet connection is required and
    for some charts a Flash player. The data remains local and is not uploaded
    to Google."""

    homepage = "https://github.com/mages/googleVis#googlevis"
    url      = "https://cran.r-project.org/src/contrib/googleVis_0.6.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/googleVis"

    version('0.6.0', 'ec36fd2a6884ddc7baa894007d0d0468')

    depends_on('r-jsonlite', type=('build', 'run'))
