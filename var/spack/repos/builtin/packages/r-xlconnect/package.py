# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RXlconnect(RPackage):
    """Provides comprehensive functionality to read, write and format Excel
    data."""

    homepage = "http://miraisolutions.wordpress.com/"
    url      = "https://cran.r-project.org/src/contrib/XLConnect_0.2-11.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/XLConnect"

    version('0.2-12', '3340d05d259f0a41262eab4ed32617ad')
    version('0.2-11', '9d1769a103cda05665df399cc335017d')

    depends_on('r-xlconnectjars', type=('build', 'run'))
    depends_on('r-rjava', type=('build', 'run'))
