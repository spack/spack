# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Opennn(CMakePackage):
    """OpenNN is a software library written in C++ for advanced analytics.
    It implements neural networks, the most successful machine learning method."""

    homepage = "https://www.opennn.net/"
    url = "https://github.com/Artelnics/opennn/archive/refs/tags/v6.0.3.tar.gz"

    version("6.0.4", sha256="3f3bcf491198444d58ea099acf69b3a4e3703b321f3fb08ad9b32e832b400c34")
    version("6.0.3", sha256="83a00039a9b6c83755ced0346437c62ebc957a96b15361b4459ac464134017b8")
    version("6.0.2", sha256="019d85dea44098964ab28cef5a928e21ea7861fef8b6f683d9ad7bccd5bb9d3a")
    version("6.0.1", sha256="2cfc7d2511d14f9ca3e090ea3f3bcf75a578eec3b6ec61afe8e0c7252532cf51")
    version("6.0.0", sha256="5d996a9fba8c4a25360ca5e2215c834264a7ba5054b7a7c8a1ce06bd10dfdd4f")
    version("5.0.5", sha256="8b8545049d085cb769f3a00e93f844061d59debab9ce514e4e91fe988e82b1ac")
    version("5.0.3", sha256="38b7a3f7c1b7b4e80db810bb48ce19572ff30c93e5eeb1b601ccfb0ea4f6dba3")
    version("5.0.0", sha256="1c3ee9afeaccfc98c4c353363468f43b29e2cc0c29418fa8e430611c72ad1414")
    version("4.9.1", sha256="fcce4215e39e33f41104022c92832e08cdd0f569576a1da2984089c70cabfcf8")
    version("4.9.0", sha256="e6b2e9adead9c2084cb83f156f5c3a079c56aef6decf2574d3731d11d741f8ba")

    depends_on("llvm-openmp")
