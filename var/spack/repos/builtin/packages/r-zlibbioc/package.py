# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RZlibbioc(RPackage):
    """This package uses the source code of zlib-1.2.5 to create libraries
       for systems that do not have these available via other means (most
       Linux and Mac users should have system-level access to zlib, and no
       direct need for this package). See the vignette for instructions
       on use."""

    homepage = "http://bioconductor.org/packages/release/bioc/html/zlibbioc.html"
    git      = "https://git.bioconductor.org/packages/zlibbioc.git"

    version('1.26.0', commit='2e3ab097caa09a5e3ddaa3469b13e19a7224da0d')
    version('1.22.0', commit='30377f830af2bc1ff17bbf3fdd2cb6442015fea5')

    depends_on('r@3.4.0:3.4.9', when='@1.22.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.26.0', type=('build', 'run'))
