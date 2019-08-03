# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSnow(RPackage):
    """Support for simple parallel computing in R."""

    homepage = "https://cloud.r-project.org/web/packages/snow/index.html"
    url      = "https://cloud.r-project.org/src/contrib/snow_0.4-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/snow"

    version('0.4-2', 'afc7b0dfd4518aedb6fc81712fd2ac70')

    depends_on('r-rmpi', type='run')
