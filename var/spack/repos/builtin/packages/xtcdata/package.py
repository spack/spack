# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xtcdata(CMakePackage):
    """LCLS II Developement: XTCData."""

    homepage = "https://github.com/slac-lcls/lcls2"
    url = "https://github.com/slac-lcls/lcls2/archive/refs/tags/3.3.37.tar.gz"

    maintainers("valmar")

    version("3.3.37", sha256="127a5ae44c9272039708bd877849a3af354ce881fde093a2fc6fe0550b698b72")

    root_cmakelists_dir = "xtcdata"
