# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGamlssData(RPackage):
    """gamlss.data: GAMLSS Data"""

    homepage = "https://cran.r-project.org/package=gamlss.data"
    url      = "https://cran.r-project.org/src/contrib/gamlss.data_5.1-0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/gamlss.data/"

    version('5.1-0', sha256='0aad438ea1aa6395677e52cd2cb496f9f4c9ba2d39edc92c8cb42e7fc91fe6c1')

    depends_on('r@2.10:', type=('build', 'run'))
