# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RHttpuv(RPackage):
    """HTTP and WebSocket Server Library.

    Provides low-level socket and protocol support for handling HTTP and
    WebSocket requests directly from within R. It is primarily intended as a
    building block for other packages, rather than making it particularly easy
    to create complete web applications using httpuv alone. httpuv is built on
    top of the libuv and http-parser C libraries, both of which were developed
    by Joyent, Inc. (See LICENSE file for libuv and http-parser license
    information.)"""

    cran = "httpuv"

    version('1.6.5', sha256='f5f63629ca5e9d0e396a89982d95b5286726c0cb425166f35a3ad32a60a79156')
    version('1.5.5', sha256='0be6c98927c7859d4bbfbbec8822c9f5e95352077d87640a76bc2ade07c83117')
    version('1.5.1', sha256='b5bb6b3b2f1a6d792568a70f3f357d6b3a35a5e26dd0c668c61a31f2ae8f5710')
    version('1.3.5', sha256='4336b993afccca2a194aca577b1975b89a35ac863423b18a11cdbb3f8470e4e9')
    version('1.3.3', sha256='bb37452ddc4d9381bee84cdf524582859af6a988e291debb71c8a2e120d02b2a')

    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
    depends_on('r-rcpp@1.0.7:', type=('build', 'run'), when='@1.6.5:')
    depends_on('r-r6', type=('build', 'run'), when='@1.5.0:')
    depends_on('r-promises', type=('build', 'run'), when='@1.5.0:')
    depends_on('r-later@0.8.0:', type=('build', 'run'), when='@1.5.0:')
    depends_on('gmake', type='build')
    depends_on('zip')

    depends_on('r-bh', type=('build', 'run'), when='@1.5.5')
