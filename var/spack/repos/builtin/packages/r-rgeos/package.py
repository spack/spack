# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRgeos(RPackage):
    """Interface to Geometry Engine - Open Source ('GEOS') using the C
    'API' for topology operations on geometries. The 'GEOS' library is
    external to the package, and, when installing the package from source,
    must be correctly installed first. Windows and Mac Intel OS X binaries
    are provided on 'CRAN'."""

    homepage = "https://cran.r-project.org/package=rgeos"
    url      = "https://cran.rstudio.com/src/contrib/rgeos_0.3-26.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/rgeos"

    version('0.3-26', '7d10a28011b49f68c5817b6fbca132df')

    depends_on('r-sp', type=('build', 'run'))
    depends_on('geos')
