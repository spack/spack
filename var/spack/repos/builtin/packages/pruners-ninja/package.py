# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PrunersNinja(AutotoolsPackage):
    """NINJA: Noise Inject agent tool to expose subtle and unintended message
    races."""

    homepage = "https://github.com/PRUNERS/NINJA"
    url = "https://github.com/PRUNERS/NINJA/releases/download/v1.0.0/NINJA-1.0.0.tar.gz"
    git = "https://github.com/PRUNERS/NINJA.git"

    version("master", branch="master")
    version("1.0.1", sha256="53df5c019054b60c68e63d3e249127f1d5f267a70539c8809fb42a8ddbfcb29b")
    version("1.0.0", sha256="f25c189783b57801f298dfff8770f42733a43f926668aceff4abd287b6e3a4d1")

    depends_on("mpi")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    patch("pruners-mutli-def-a-pr3-fix.patch")
