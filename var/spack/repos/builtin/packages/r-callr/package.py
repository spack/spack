# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCallr(RPackage):
    """It is sometimes useful to perform a computation in a separate R
       process, without affecting the current R process at all. This packages
       does exactly that."""

    homepage = "https://github.com/MangoTheCat/callr"
    url      = "https://cran.r-project.org/src/contrib/callr_1.0.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/callr/"

    version('3.0.0', sha256='e36361086c65660a6ecbbc09b5ecfcddee6b59caf75e983e48b21d3b8defabe7')
    version('1.0.0', 'd9af99bb95696310fa1e5d1cb7166c91')
