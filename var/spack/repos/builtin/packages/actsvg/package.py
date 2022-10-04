# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Actsvg(CMakePackage):
    """An SVG based C++17 plotting library for ACTS detectors and
    surfaces."""

    homepage = "https://github.com/acts-project/actsvg"
    url = "https://github.com/acts-project/actsvg/archive/refs/tags/v0.4.22.zip"
    list_url = "https://github.com/acts-project/actsvg/releases"
    git = "https://github.com/acts-project/actsvg.git"

    maintainers = ["HadrienG2", "wdconinc"]

    version("0.4.22", sha256="a535dc80b309033c45a8521c01b5ea6cd82c1fc8c89661d112de8879d68be790")

    variant(
        "examples",
        default=False,
        description="Build the example applications",
    )
    variant(
        "meta",
        default=True,
        description="Build the meta level interface",
    )

    def cmake_args(self):
        args = [
            self.define_from_variant("ACTSVG_BUILD_EXAMPLES", "examples"),
            self.define_from_variant("ACTSVG_BUILD_META", "meta"),
            self.define("ACTSVG_BUILD_TESTING", self.run_tests),
        ]
        return args
