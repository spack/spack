# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

from spack.package import *


class Tioga(CMakePackage):
    """Topology Independent Overset Grid Assembly (TIOGA)"""

    homepage = "https://github.com/jsitaraman/tioga"
    git = "https://github.com/jsitaraman/tioga.git"

    maintainers("jrood-nrel")

    license("LGPL-3.0-only")

    # The original TIOGA repo has been abandoned,
    # so work on TIOGA has continued in the Exawind project
    version("develop", git="https://github.com/Exawind/tioga.git", branch="exawind")
    version(
        "1.3.0",
        git="https://github.com/Exawind/tioga.git",
        tag="v1.3.0",
        commit="b1c018a1f8c266e5984a57cc69462625e92d6678",
    )
    version(
        "1.2.0",
        git="https://github.com/Exawind/tioga.git",
        tag="v1.2.0",
        commit="cbff5456ca339bae9ebe8e3e1aac5108695e8359",
    )
    version(
        "1.1.0",
        git="https://github.com/Exawind/tioga.git",
        tag="v1.1.0",
        commit="03f7515f10d9523c0b59dd270f310a3b7eb6ddef",
    )
    version(
        "1.0.0",
        git="https://github.com/Exawind/tioga.git",
        tag="v1.0.0",
        commit="d1f0ceb5db5cffecc3197a904fbf4d539d87e6a1",
    )
    version("master", branch="master")

    depends_on("cxx", type="build")

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
