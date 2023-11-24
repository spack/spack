# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Csblast(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://wwwuser.gwdg.de/~compbiol/data/csblast/releases"
    url = "http://wwwuser.gwdg.de/~compbiol/data/csblast/releases/csblast-2.2.3_linux64.tar.gz"

    version("2.2.3", sha256="36fae7a9d2e5673015d19d34d2d55551b4e37bc3db2fcb7f2380ac6eba556599")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.data)
        install_tree("bin", prefix.bin)
        install_tree("data", prefix.data)
