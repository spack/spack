# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hyperfine(Package):
    """A command-line benchmarking tool."""

    homepage = "https://github.com/sharkdp/hyperfine"
    url = "https://github.com/sharkdp/hyperfine/archive/refs/tags/v1.12.0.tar.gz"

    maintainers("michaelkuhn")

    version("1.17.0", sha256="3dcd86c12e96ab5808d5c9f3cec0fcc04192a87833ff009063c4a491d5487b58")
    version("1.16.1", sha256="ffb3298945cbe2c068ca1a074946d55b9add83c9df720eda2ed7f3d94d7e65d2")
    version("1.14.0", sha256="59018c22242dd2ad2bd5fb4a34c0524948b7921d02aa79419ccec4c1ffd3da14")
    version("1.13.0", sha256="6e57c8e51962dd24a283ab46dde6fe306da772f4ef9bad86f8c89ac3a499c87e")
    version("1.12.0", sha256="2120870a97e68fa3426eac5646a071c9646e96d2309220e3c258bf588e496454")

    depends_on("rust@1.46:")

    def install(self, spec, prefix):
        cargo = which("cargo")
        cargo("install", "--root", prefix, "--path", ".")
