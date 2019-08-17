# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTestthat(RPackage):
    """A unit testing system designed to be fun, flexible and easy to set
    up."""

    homepage = "https://github.com/hadley/testthat"
    url      = "https://cloud.r-project.org/src/contrib/testthat_1.0.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/testthat"

    version('2.2.1', sha256='67ee0512bb312695c81fd74338bb8ce9e2e58763681ddbcdfdf35f52dfdb0b78')
    version('2.1.0', sha256='cf5fa7108111b32b86e70819352f86b57ab4e835221bb1e83642d52a1fdbcdd4')
    version('1.0.2', '6c6a90c8db860292df5784a70e07b8dc')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-crayon@1.3.4:', type=('build', 'run'))
    depends_on('r-praise', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-r6@2.2.0:', type=('build', 'run'))
    depends_on('r-cli', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-rlang@0.3.0:', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-withr@2.0.0:', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-evaluate', when='@2.2.0:', type=('build', 'run'))
