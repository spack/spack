# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RKnitr(RPackage):
    """Provides a general-purpose tool for dynamic report generation in R using
    Literate Programming techniques."""

    homepage = "https://cloud.r-project.org/package=knitr"
    url      = "https://cloud.r-project.org/src/contrib/knitr_1.14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/knitr"

    version('1.24', sha256='e80c2043b445a7e576b62ae8510cce89322660fe388881d799a706d35cd27b89')
    version('1.23', sha256='063bfb3300fc9f3e7d223c346e19b93beced0e6784470b9bef2524868a206a99')
    version('1.17', '4407ccf8f2a51629800d6d5243cf3e70')
    version('1.14', 'ef0fbeaa9372f99ffbc57212a7781511')
    version('0.6',  'c67d6db84cd55594a9e870c90651a3db')

    depends_on('r@2.14.1:', when='@:1.9', type=('build', 'run'))
    depends_on('r@3.0.2:', when='@1.10:1.14', type=('build', 'run'))
    depends_on('r@3.1.0:', when='@1.15:1.22', type=('build', 'run'))
    depends_on('r@3.2.3:', when='@1.23:', type=('build', 'run'))
    depends_on('r-evaluate@0.10:', type=('build', 'run'))
    depends_on('r-digest@:1.17', type=('build', 'run'))
    depends_on('r-formatr@:1.14', type=('build', 'run'))
    depends_on('r-highr', type=('build', 'run'))
    depends_on('r-stringr@0.6:', type=('build', 'run'))
    depends_on('r-markdown', type=('build', 'run'))
    depends_on('r-yaml@2.1.19:', type=('build', 'run'))
    depends_on('r-xfun', when='@1.23:', type=('build', 'run'))
