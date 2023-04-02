# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sdl2Ttf(CMakePackage):
    """Simple DirectMedia Layer 2 TrueType Fonts library"""

    homepage = "https://www.libsdl.org/projects/SDL_ttf/"
    url = "https://www.libsdl.org/projects/SDL_ttf/release/SDL2_ttf-2.20.2.tar.gz"
    git = "https://github.com/libsdl-org/SDL_ttf.git"

    version("2.20.2", sha256="9dc71ed93487521b107a2c4a9ca6bf43fb62f6bddd5c26b055e6b91418a22053")
    version("2.20.1", sha256="78cdad51f3cc3ada6932b1bb6e914b33798ab970a1e817763f22ddbfd97d0c57")
    version("2.0.18", sha256="7234eb8883514e019e7747c703e4a774575b18d435c22a4a29d068cb768a2251")
    version("2.0.15", sha256="a9eceb1ad88c1f1545cd7bd28e7cbc0b2c14191d40238f531a15b01b1b22cd33")
    version("2.0.14", sha256="34db5e20bcf64e7071fe9ae25acaa7d72bdc4f11ab3ce59acc768ab62fe39276")
    version("2.0.13", sha256="f51d3829985691efa9aad306a935ef69bc880a525c887548563c33ea35e8ed04")
    version("2.0.12", sha256="8728605443ea1cca5cad501dc34dc0cb15135d1e575551da6d151d213d356f6e")

    depends_on("sdl2")



