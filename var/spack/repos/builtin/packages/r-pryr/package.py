# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RPryr(RPackage):
    """Useful tools to pry back the covers of R and understand the language
    at a deeper level."""

    homepage = "https://github.com/hadley/pryr"
    url      = "https://cran.r-project.org/src/contrib/pryr_0.1.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/pryr"

    version('0.1.2', '66b597a762aa15a3b7037779522983b6')

    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
