# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Meshlab(CMakePackage):
    """The open source mesh processing system."""

    homepage = "https://www.meshlab.net"
    url = "https://github.com/cnr-isti-vclab/meshlab/archive/refs/tags/MeshLab-2023.12.tar.gz"
    git = "https://github.com/cnr-isti-vclab/meshlab.git"

    maintainers("wdconinc")

    license("GPL-3.0", checked_by="wdconinc")

    version("main", branch="main", submodules=True)
    version("2023.12", commit="2dbd2f4b12df3b47d8777b2b4a43cabd9e425735", submodules=True)

    variant("double_scalar", default=False, description="Type to use for scalars")

    depends_on("eigen")
    depends_on("glew")
    depends_on("mpfr")
    depends_on("qt@5.15: +opengl")

    def cmake_args(self):
        args = [
            self.define_from_variant("MESHLAB_BUILD_WITH_DOUBLE_SCALAR", "double_scalar"),
        ]
        return args
