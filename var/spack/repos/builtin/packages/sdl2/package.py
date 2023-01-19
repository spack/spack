# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Sdl2(CMakePackage):
    """Simple DirectMedia Layer is a cross-platform development library
    designed to provide low level access to audio, keyboard, mouse, joystick,
    and graphics hardware via OpenGL and Direct3D."""

    homepage = "https://wiki.libsdl.org/FrontPage"
    url = "https://libsdl.org/release/SDL2-2.0.5.tar.gz"
    git = "https://github.com/libsdl-org/SDL.git"
    list_url = "https://github.com/libsdl-org/SDL.git"

    version("2.24.1", sha256="bc121588b1105065598ce38078026a414c28ea95e66ed2adab4c44d80b309e1b")
    version("2.0.22", sha256="fe7cbf3127882e3fc7259a75a0cb585620272c51745d3852ab9dd87960697f2e")
    version("2.0.14", sha256="d8215b571a581be1332d2106f8036fcb03d12a70bae01e20f424976d275432bc")
    version("2.0.5", sha256="442038cf55965969f2ff06d976031813de643af9c9edc9e331bd761c242e8785")

    depends_on("cmake@2.8.5:", type="build")
    if sys.platform.startswith("linux"):
        depends_on("libxext", type="link")

    def cmake_args(self):
        return ["-DSSEMATH={0}".format("OFF" if self.spec.target.family == "aarch64" else "ON")]
