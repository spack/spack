# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

from spack.package import *


class Tioga(CMakePackage):
    """Topology Independent Overset Grid Assembly (TIOGA)"""

    homepage = "https://github.com/jsitaraman/tioga"
    git = "https://github.com/jsitaraman/tioga.git"

    maintainers("jrood-nrel")

    # The original TIOGA repo has possibly been abandoned,
    # so work on TIOGA has continued in the Exawind project
    version("develop", git="https://github.com/Exawind/tioga.git", branch="exawind")
    version("master", branch="master")

    variant("shared", default=sys.platform != "darwin", description="Build shared libraries")
    variant("pic", default=True, description="Position independent code")
    variant("nodegid", default=True, description="Enable support for global Node IDs")
    variant("timers", default=False, description="Enable timers")
    variant("stats", default=False, description="Enable output of holecut stats")

    depends_on("mpi")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            self.define_from_variant("TIOGA_HAS_NODEGID", "nodegid"),
            self.define_from_variant("TIOGA_ENABLE_TIMERS", "timers"),
            self.define_from_variant("TIOGA_OUTPUT_STATS", "stats"),
        ]

        return args
