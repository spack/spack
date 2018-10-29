# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMulticool(RPackage):
    """Permutations of multisets in cool-lex order."""

    homepage = "https://cran.r-project.org/package=multicool"
    url      = "https://cran.r-project.org/src/contrib/multicool_0.1-10.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/multicool/"

    version('0.1-10', sha256='5bb0cb0d9eb64420c862877247a79bb0afadacfe23262ec8c3fa26e5e34d6ff9')
    version('0.1-9', sha256='bdf92571cef1b649952d155395a92b8683099ee13114f73a9d41fc5d7d49d329')

    depends_on('r-rcpp@0.11.2:', type=('build', 'run'))
