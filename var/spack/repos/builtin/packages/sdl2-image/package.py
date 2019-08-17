# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sdl2Image(AutotoolsPackage):
    """SDL is designed to provide the bare bones of creating a graphical
    program. """

    homepage = "http://sdl.beuc.net/sdl.wiki/SDL_image"
    url      = "https://www.libsdl.org/projects/SDL_image/release/SDL2_image-2.0.1.tar.gz"

    version('2.0.1', 'd94b94555ba022fa249a53a021dc3606')

    depends_on('sdl2')
