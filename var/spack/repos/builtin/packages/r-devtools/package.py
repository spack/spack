# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDevtools(RPackage):
    """Collection of package development tools."""

    homepage = "https://github.com/hadley/devtools"
    url      = "https://cloud.r-project.org/src/contrib/devtools_1.12.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/devtools"

    version('2.1.0', sha256='c1f75346a90adf0669b5508fe68cc78bd3b114c1303fa7d22bf90991edd9230d')
    version('2.0.2', sha256='99a2fa957068254b8ecdb3fc2d50e2950230910ea31c314fc0e7d934e4bd1709')
    version('1.12.0', sha256='8a3e2ca3988dffe29341e45a160bb588995eae43485d6a811a9ae4836d37afd4')
    version('1.11.1', sha256='51c876f9ddbfdf611f6ea0b06c0b46da8cefcb8cc98d60e06d576b61f0a06346')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r-httr@0.4:', type=('build', 'run'))
    depends_on('r-memoise@1.0.0:', type=('build', 'run'))
    depends_on('r-whisker', when='@:1.9.9', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-rstudioapi@0.7.0:', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-git2r@0.23.0:', type=('build', 'run'))
    depends_on('r-withr', type=('build', 'run'))
    depends_on('r-usethis@1.5.0:', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-callr', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-cli', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-pkgbuild@1.0.3:', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-pkgload@1.0.2:', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-rcmdcheck@1.3.3:', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-remotes@2.1.0:', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-roxygen2@6.1.1:', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-sessioninfo@1.1.1:', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-testthat@2.1.1:', when='@2.0.0:', type=('build', 'run'))
