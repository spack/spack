# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Uncrustify(CMakePackage, AutotoolsPackage):
    """Source Code Beautifier for C, C++, C#, ObjectiveC, Java, and others."""

    homepage = "http://uncrustify.sourceforge.net/"
    git = "https://github.com/uncrustify/uncrustify"
    url = "https://sourceforge.net/projects/uncrustify/files/uncrustify/uncrustify-0.69/uncrustify-0.69.tar.gz"

    maintainers("gmaurel")

    version("master", branch="master")
    version("0.74", commit="62048b")
    version("0.73", commit="25b765")
    version("0.72", commit="1d3d8f")
    version("0.71", commit="64d82f")
    version("0.70", commit="51f64d")
    version("0.69", commit="a7a8fb")
    version("0.68", commit="86bc34")
    version("0.67", commit="00321a")
    version("0.66", commit="80f549")
    version("0.65", commit="905676")
    version("0.64", commit="1d7d97")
    version("0.63", commit="44ce0f")
    version("0.62", commit="5987f2")
    version("0.61", sha256="1df0e5a2716e256f0a4993db12f23d10195b3030326fdf2e07f8e6421e172df9")

    build_system(
        conditional("cmake", when="@0.64:"),
        conditional("autotools", when="@:0.63"),
        default="cmake",
    )

    with when("build_system=autotools"):
        depends_on("automake", type="build")
        depends_on("autoconf", type="build")
        depends_on("libtool", type="build", when="@0.63")

    patch("uncrustify-includes.patch", when="@0.73")
