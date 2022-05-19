# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tracy(MakefilePackage):
    """A real time, nanosecond resolution, remote telemetry, hybrid frame and sampling
    profiler for games and other applications. Server applications."""

    homepage = "https://github.com/wolfpld/tracy"
    url = "https://github.com/wolfpld/tracy/archive/v0.0.0.tar.gz"
    maintainers = ["msimberg"]

    version("master", git="https://github.com/wolfpld/tracy.git", branch="master")
    version(
        "0.8.1",
        sha256="004992012b2dc879a9f6d143cbf94d7ea30e88135db3ef08951605d214892891",
    )

    depends_on("capstone")
    depends_on("dbus")
    depends_on("freetype")
    # Linking fails unless glfw is built as a shared library:
    # https://github.com/wolfpld/tracy/issues/110
    depends_on("glfw +shared")

    def build(self, spec, prefix):
        with working_dir(join_path(self.build_directory, "capture/build/unix")):
            make()

        with working_dir(join_path(self.build_directory, "profiler/build/unix")):
            make()

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install(
            join_path(self.build_directory, "capture/build/unix/capture-release"),
            prefix.bin,
        )
        install(
            join_path(self.build_directory, "profiler/build/unix/Tracy-release"),
            prefix.bin,
        )
