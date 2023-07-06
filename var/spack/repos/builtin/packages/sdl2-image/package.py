# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sdl2Image(AutotoolsPackage):
    """SDL is designed to provide the bare bones of creating a graphical
    program."""

    homepage = "http://sdl.beuc.net/sdl.wiki/SDL_image"
    url = "https://www.libsdl.org/projects/SDL_image/release/SDL2_image-2.0.1.tar.gz"

    version("2.6.3", sha256="931c9be5bf1d7c8fae9b7dc157828b7eee874e23c7f24b44ba7eff6b4836312c")
    version("2.0.1", sha256="3a3eafbceea5125c04be585373bfd8b3a18f259bd7eae3efc4e6d8e60e0d7f64")

    depends_on("sdl2")
