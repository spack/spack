# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPkgbuild(RPackage):
    """pkgbuild: Find Tools Needed to Build R Packages"""

    homepage = "https://cloud.r-project.org/package=pkgbuild"
    url      = "https://cloud.r-project.org/src/contrib/pkgbuild_1.0.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pkgbuild/"

    version('1.0.4', sha256='2934efa5ff9ccfe1636d360aedec36713f3bb3128a493241dbb728d842ea3b5f')
    version('1.0.3', sha256='c93aceb499886e42bcd61eb7fb59e47a76c9ba5ab5349a426736d46c8ce21f4d')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-callr@2.0.0:', when='@:1.0.3', type=('build', 'run'))
    depends_on('r-callr@3.2.0:', when='@1.0.4:', type=('build', 'run'))
    depends_on('r-cli', type=('build', 'run'))
    depends_on('r-crayon', type=('build', 'run'))
    depends_on('r-desc', type=('build', 'run'))
    depends_on('r-prettyunits', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-rprojroot', type=('build', 'run'))
    depends_on('r-withr@2.1.2:', type=('build', 'run'))
