# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSnow(RPackage):
    """Support for simple parallel computing in R."""

    homepage = "https://cloud.r-project.org/package=snow"
    url      = "https://cloud.r-project.org/src/contrib/snow_0.4-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/snow"

    version('0.4-3', sha256='8512537daf334ea2b8074dbb80cf5e959a403a78d68bc1e97664e8a4f64576d8')
    version('0.4-2', 'afc7b0dfd4518aedb6fc81712fd2ac70')

    depends_on('r@2.13.1:', type=('build', 'run'))
