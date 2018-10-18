# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTestthat(RPackage):
    """A unit testing system designed to be fun, flexible and easy to set
    up."""

    homepage = "https://github.com/hadley/testthat"
    url      = "https://cran.r-project.org/src/contrib/testthat_1.0.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/testthat"

    version('1.0.2', '6c6a90c8db860292df5784a70e07b8dc')

    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-crayon', type=('build', 'run'))
    depends_on('r-praise', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
