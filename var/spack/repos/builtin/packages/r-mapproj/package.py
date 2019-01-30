# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMapproj(RPackage):
    """Converts latitude/longitude into projected coordinates."""

    homepage = "https://cran.r-project.org/package=mapproj"
    url      = "https://cran.r-project.org/src/contrib/mapproj_1.2-4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mapproj"

    version('1.2-4', '10e22bde1c790e1540672f15ddcaee71')

    depends_on('r-maps', type=('build', 'run'))
