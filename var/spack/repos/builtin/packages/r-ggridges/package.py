# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGgridges(RPackage):
    """Ridgeline plots provide a convenient way of visualizing changes in
    distributions over time or space."""

    homepage = "https://cloud.r-project.org/package=ggridges"
    url      = "https://cloud.r-project.org/src/contrib/ggridges_0.4.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggridges"

    version('0.5.1', sha256='01f87cdcdf2052ed9c078d9352465cdeda920a41e2ca55bc154c1574fc651c36')
    version('0.5.0', sha256='124bc84044e56728fa965682f8232fc868f2af7d3eb7276f6b0df53be8d2dbfe')
    version('0.4.1', '21d53b3f7263beb17f629f0ebfb7b67a')
    version('0.4.0', 'da94ed1ee856a7fa5fb87712c84ec4c9')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r-ggplot2@2.2.0:', type=('build', 'run'))
    depends_on('r-plyr@1.8.0:', type=('build', 'run'))
    depends_on('r-scales@0.4.1:', type=('build', 'run'))
    depends_on('r-withr@2.1.1:', when='@0.5.0:', type=('build', 'run'))
