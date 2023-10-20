# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CubeTauvalue(AutotoolsPackage):
    """Plugin to display TAU statistics in form of a box plot in CubeGUI"""

    homepage = "https://www.scalasca.org/software/cube-4.x/download.html"
    url = "https://apps.fz-juelich.de/scalasca/releases/cube/4.8/dist/tauvalueview-v0.3.tar.gz"
    maintainers("swat-jsc")

    version("0.3", sha256="95c6562867497c0982adcb63c03f514df7b251ac101f06e0d827b2d252d85aeb")
    depends_on("cube@4.8:+gui")
    depends_on("cubelib@4.8:")
    depends_on("qt@5.9.1:")
