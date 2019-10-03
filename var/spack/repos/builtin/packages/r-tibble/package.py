# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTibble(RPackage):
    """Provides a 'tbl_df' class that offers better checking and printing
    capabilities than traditional data frames."""

    homepage = "https://github.com/tidyverse/tibble"
    url      = "https://cloud.r-project.org/src/contrib/tibble_1.3.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tibble"

    version('2.1.3', sha256='9a8cea9e6b5d24a7e9bf5f67ab38c40b2b6489eddb0d0edb8a48a21ba3574e1a')
    version('2.0.1', sha256='7ab2cc295eecf00a5310993c99853cd6622ad468e7a60d004b8a73957a713d13')
    version('2.0.0', sha256='05ad2d62e949909548c4bb8ac596810321f11b330afa9717d0889dc35edd99ba')
    version('1.4.2', sha256='11670353ff7059a55066dd075d1534d6a27bc5c3583fb9bc291bf750a75c5b17')
    version('1.4.1', sha256='32267fae1ca86abdd37c4683f9d2b1a47b8b65e1977ea3900aa197066c57aa29')
    version('1.3.4', '298e81546f999fb0968625698511b8d3')
    version('1.2', 'bdbc3d67aa16860741add6d6ec20ea13')
    version('1.1', '2fe9f806109d0b7fadafb1ffafea4cb8')

    depends_on('r@3.1.0:', when='@1.3.0:', type=('build', 'run'))
    depends_on('r@3.1.2:', when='@:1.2', type=('build', 'run'))
    depends_on('r-assertthat', type=('build', 'run'), when='@:1.3.1')
    depends_on('r-lazyeval@0.1.10:', type=('build', 'run'), when='@:1.3.0')
    depends_on('r-rcpp@0.12.3:', type=('build', 'run'), when='@:1.3.4')
    depends_on('r-rlang@0.3.0:', type=('build', 'run'), when='@1.3.1:')
    depends_on('r-cli', type=('build', 'run'), when='@1.4.2:')
    depends_on('r-crayon@1.3.4:', type=('build', 'run'), when='@1.4.1:')
    depends_on('r-pillar@1.3.1:', type=('build', 'run'), when='@1.4.1:')
    depends_on('r-pkgconfig', type=('build', 'run'), when='@2.0.0:')
    depends_on('r-fansi@0.4.0:', type=('build', 'run'), when='@2.0.0:')
