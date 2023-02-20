# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Actsvg(CMakePackage):
    """An SVG based C++17 plotting library for ACTS detectors and
    surfaces."""

    homepage = "https://github.com/acts-project/actsvg"
    url = "https://github.com/acts-project/actsvg/archive/refs/tags/v0.4.22.zip"
    list_url = "https://github.com/acts-project/actsvg/tags"
    git = "https://github.com/acts-project/actsvg.git"

    maintainers("HadrienG2", "wdconinc")

    version("0.4.28", sha256="12c6f0c41b1aeb21164c949498819976bf91a395968debcb400539713bdfc6b0")
    version("0.4.27", sha256="f4b06ad6d0f424505f3b1315503c3197bebb24c900a498bda12c453919b06d27")
    version("0.4.26", sha256="a1dfad15b616cac8191a355c1a87544571c36349400e3de56b9e5be6fa73714c")

    variant("examples", default=False, description="Build the example applications")
    variant("meta", default=True, description="Build the meta level interface")

    depends_on("boost +program_options", type="test")
    depends_on("boost +program_options", when="+examples")
    depends_on("googletest", when="+examples")

    def cmake_args(self):
        args = [
            self.define_from_variant("ACTSVG_BUILD_EXAMPLES", "examples"),
            self.define_from_variant("ACTSVG_BUILD_META", "meta"),
            self.define("ACTSVG_BUILD_TESTING", self.run_tests),
        ]
        return args
