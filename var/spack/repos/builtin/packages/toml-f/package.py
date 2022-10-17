# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TomlF(MesonPackage):
    """
    TOML parser implementation for data serialization and deserialization in Fortran
    """

    homepage = "https://toml-f.readthedocs.io"
    url = "https://github.com/toml-f/toml-f/releases/download/v0.2.3/toml-f-0.2.3.tar.xz"
    git = "https://github.com/toml-f/toml-f.git"

    maintainers = ["awvwgk"]

    version("main", branch="main")
    version("0.3.0", "40ceca008091607165a09961b79312abfdbbda71cbb94a9dc2625b88c93ff45a")
    version("0.2.3", "2dca7ff6d3e35415cd92454c31560d2b656c014af8236be09c54c13452e4539c")

    depends_on("meson@0.57.2:", type="build")

    def meson_args(self):
        return [
            "--wrap-mode=nodownload",
        ]
