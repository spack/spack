# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RXmapbridge(RPackage):
    """xmapBridge can plot graphs in the X:Map genome browser. This package
       exports plotting files in a suitable format."""

    homepage = "https://www.bioconductor.org/packages/xmapbridge/"
    git      = "https://git.bioconductor.org/packages/xmapbridge.git"

    version('1.34.0', commit='f162e1f72ead5f5a1aede69032d5771a6572d965')

    depends_on('r@3.4.0:3.4.9', when='@1.34.0')
