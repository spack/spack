# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPkgbuild(RPackage):
    """pkgbuild: Find Tools Needed to Build R Packages"""

    homepage = "https://cran.r-project.org/package=pkgbuild"
    url      = "https://cran.r-project.org/src/contrib/pkgbuild_1.0.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/pkgbuild/"

    version('1.0.3', sha256='c93aceb499886e42bcd61eb7fb59e47a76c9ba5ab5349a426736d46c8ce21f4d')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-callr', type=('build', 'run'))
    depends_on('r-cli', type=('build', 'run'))
    depends_on('r-crayon', type=('build', 'run'))
    depends_on('r-desc', type=('build', 'run'))
    depends_on('r-prettyunits', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-rprojroot', type=('build', 'run'))
    depends_on('r-withr', type=('build', 'run'))
