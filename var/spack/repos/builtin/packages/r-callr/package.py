# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCallr(RPackage):
    """It is sometimes useful to perform a computation in a separate R
       process, without affecting the current R process at all. This packages
       does exactly that."""

    homepage = "https://github.com/MangoTheCat/callr"
    url      = "https://cloud.r-project.org/src/contrib/callr_1.0.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/callr/"

    version('3.3.1', sha256='bf60da47357d3336aa395b0c9643235a621763c80d28bc9bb2257767d0a37967')
    version('3.2.0', sha256='4bb47b1018e8eb5c683a86c05d0d9b8b25848db1f1b30e92cfebedc0ce14b0e8')
    version('3.0.0', sha256='e36361086c65660a6ecbbc09b5ecfcddee6b59caf75e983e48b21d3b8defabe7')
    version('1.0.0', 'd9af99bb95696310fa1e5d1cb7166c91')

    depends_on('r-processx@3.4.0:', type=('build', 'run'), when='@3.0.0:')
    depends_on('r-r6', type=('build', 'run'), when='@3.0.0:')
