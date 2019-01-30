# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCtc(RPackage):
    """Tools for export and import classification trees and clusters
       to other programs"""

    homepage = "https://www.bioconductor.org/packages/release/bioc/html/ctc.html"
    git      = "https://git.bioconductor.org/packages/ctc.git"

    version('1.54.0', commit='0c3df81dfc8fabe12e11884bed44b64e11fd6d4e')

    depends_on('r-amap', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.54.0:', type=('build', 'run'))
