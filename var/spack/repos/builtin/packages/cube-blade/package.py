# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CubeBlade(AutotoolsPackage):
    """Simple OTF2 trace explorer"""

    homepage = "https://www.scalasca.org/software/cube-4.x/download.html"
    url = "https://apps.fz-juelich.de/scalasca/releases/cube/4.8/dist/blade-0.5.tar.gz"
    maintainers("swat-jsc")

    version("0.5", sha256="0770cd4c2e1b8f31bdb6dadf39232b709aee869835e12f9e1ac670d0b276a689")

    depends_on("cube@4.8:+gui")
    depends_on("cubelib@4.8:")
    depends_on("qt@5.9.1:")
    depends_on("otf2@3.0:")

    # Without this patch, the Blade plugin crashes Cube on startup
    patch("return-bool.patch")
