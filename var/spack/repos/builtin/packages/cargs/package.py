# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cargs(CMakePackage):
    """A lightweight cross-platform C/C++ getopt alternative that works on
    Linux, Windows and macOS."""

    homepage = "https://likle.github.io/cargs/"
    url = "https://github.com/likle/cargs/archive/refs/tags/v1.0.3.tar.gz"
    git = "https://github.com/likle/cargs.git"

    version("1.0.3", sha256="ddba25bd35e9c6c75bc706c126001b8ce8e084d40ef37050e6aa6963e836eb8b")

    depends_on("cmake@3.14.7:", type=("build"))
