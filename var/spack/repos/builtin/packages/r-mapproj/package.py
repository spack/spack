# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMapproj(RPackage):
    """Converts latitude/longitude into projected coordinates."""

    homepage = "https://cran.r-project.org/package=mapproj"
    url      = "https://cran.r-project.org/src/contrib/mapproj_1.2-4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mapproj"

    version('1.2-5', sha256='f3026a3a69a550c923b44c18b1ccc60d98e52670a438250d13f3c74cf2195f66')
    version('1.2-4', '10e22bde1c790e1540672f15ddcaee71')

    depends_on('r-maps', type=('build', 'run'))
