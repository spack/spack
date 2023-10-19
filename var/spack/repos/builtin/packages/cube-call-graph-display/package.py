# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CubeCallGraph(AutotoolsPackage):
    """Call raph display for CubeGUI"""

    homepage = "https://www.scalasca.org/software/cube-4.x/download.html"
    url = "https://apps.fz-juelich.de/scalasca/releases/cube/4.8/dist/callgraph-v0.4.tar.gz"
    maintainers="swat-jsc"

    version("v0.4", sha256="796dd24d130864d15fdb82f9a02008aa0a37e13600c176299d6fe3cc1f9845af")

    depends_on("cube@4.8:")
    depends_on("cubelib@4.8:")
    depends_on("qt@5.9.1:")
