# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGeosphere(RPackage):
    """Spherical trigonometry for geographic applications. That is, compute
    distances and related measures for angular (longitude/latitude)
    locations."""

    homepage = "https://cran.r-project.org/package=geosphere"
    url      = "https://cran.r-project.org/src/contrib/geosphere_1.5-5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/geosphere"

    version('1.5-5', '28efb7a8e266c7f076cdbcf642455f3e')

    depends_on('r-sp', type=('build', 'run'))
