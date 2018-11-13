# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPs(RPackage):
    """Manipulate processes on Windows, Linux and MacOS"""

    homepage = "https://github.com/r-lib/ps"
    url      = "https://cran.r-project.org/src/contrib/ps_1.1.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ps/ps_1.0.0.tar.gz"

    version('1.1.0', sha256='5d5240d5bf1d48c721b3fdf47cfc9dbf878e388ea1f057b764db05bffdc4a9fe')
    version('1.0.0', sha256='9bdaf64aaa44ae11866868402eb75bf56c2e3022100476d9b9dcd16ca784ffd8')
