# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFarver(RPackage):
    """farver: High Performance Colour Space Manipulation"""

    homepage = "https://github.com/thomasp85/farver"
    url      = "https://cloud.r-project.org/src/contrib/farver_2.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/farver"

    version('2.0.3', sha256='0e1590df79ec6078f10426411b96216b70568a4eaf3ffd84ca723add0ed8e5cc')
    version('2.0.1', sha256='71473e21727357084c6aec4bb9bb258a6797a0f676b4b27504a03f16aa2f4e54')
