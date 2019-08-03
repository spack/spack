# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGeosphere(RPackage):
    """Spherical trigonometry for geographic applications. That is, compute
    distances and related measures for angular (longitude/latitude)
    locations."""

    homepage = "https://cloud.r-project.org/package=geosphere"
    url      = "https://cloud.r-project.org/src/contrib/geosphere_1.5-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/geosphere"

    version('1.5-7', sha256='9d9b555e2d59a5ae174ae654652121f169fbc3e9cf66c2491bfbe0684b6dd8a0')
    version('1.5-5', '28efb7a8e266c7f076cdbcf642455f3e')

    depends_on('r-sp', type=('build', 'run'))
