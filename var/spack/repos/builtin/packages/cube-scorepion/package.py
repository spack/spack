# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CubeScorePion(AutotoolsPackage):
    """Score-P filter creation in CubeGUI"""

    homepage = "https://www.scalasca.org/software/cube-4.x/download.html"
    url = "https://apps.fz-juelich.de/scalasca/releases/cube/4.8/dist/scorepion-v0.5.tar.gz"
    maintainers = "swat-jsc"

    version("v0.5", sha256="ff9ed6afc5e46bc54e29bba2d5d1bd8d9fae4a042aa7090791d6b5033370678a")

    depends_on("cube@4.8:")
    depends_on("cubelib@4.8:")
    depends_on("qt@5.9.1:")
    depends_on("scorep@7.0:")
