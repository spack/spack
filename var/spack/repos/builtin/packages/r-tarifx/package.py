# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTarifx(RPackage):
    """A collection of various utility and convenience functions."""

    homepage = "https://cloud.r-project.org/package=taRifx"
    url      = "https://cloud.r-project.org/src/contrib/taRifx_1.0.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/taRifx"

    version('1.0.6.1', sha256='d4c832b26d476a395ddf8349c42613270023c8bbf52a274d280be6284c11d7e2')
    version('1.0.6', '7e782e04bd69d929b29f91553382e6a2')

    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
