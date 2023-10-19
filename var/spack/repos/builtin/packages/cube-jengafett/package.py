# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CubeJengaFett(AutotoolsPackage):
    """Metrics correlation display as stacked bars in CubeGUI"""

    homepage = "https://www.scalasca.org/software/cube-4.x/download.html"
    url = "https://apps.fz-juelich.de/scalasca/releases/cube/4.8/dist/jengafett-v0.5.tar.gz"
    maintainers = "swat-jsc"

    version("v0.5", sha256="60bc00018cf2d48039b1ea5c159e0503598fa1dfe081bc3ec1e3b0d4952e180d")

    depends_on("cube@4.8:")
    depends_on("cubelib@4.8:")
    depends_on("qt@5.9.1:")
