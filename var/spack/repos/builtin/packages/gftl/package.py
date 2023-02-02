# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Gftl(CMakePackage):
    """This package generates containers (Vector, Set, Map, ...) with
    Fortran interfaces. It is essentially a brute force analog of C++
    STL.

    This package, gFTL, provides a mechanism to easily create robust
    containers and associated iterators which can be used within Fortran
    applications. The primary methods are intended to be as close
    to their C++ STL analogs as possible. We have found that these
    containers are a powerful productivity multiplier for certain types
    of software development, and hope that others find them to be just
    as useful.

    Currently, the following three types of containers are provided.

    * Vector (list)
    * Set
    * Map (associated array)

    Contributions of additional containers are very much welcomed.
    """

    homepage = "https://github.com/Goddard-Fortran-Ecosystem/gFTL"
    url = "https://github.com/Goddard-Fortran-Ecosystem/gFTL/archive/refs/tags/v1.5.5.tar.gz"
    git = "https://github.com/Goddard-Fortran-Ecosystem/gFTL.git"

    maintainers("mathomp4", "tclune")

    version("develop", branch="develop")
    version("main", branch="main")

    version("1.8.2", sha256="7ee9a1db62f6dd09e533516d7dc53fbc9c8c81464bb12f6eb558ad5d3bfd85ef")
    version("1.8.1", sha256="b8171ea69b108325816472ee47068618d709a3f563959142bc58ff38908a7210")
    version("1.8.0", sha256="e99def0a9a1b3031ceff22c416bee75e70558cf6b91ce4be70b0ad752dda26c6")
    version("1.7.2", sha256="35a39a0dffb91969af5577b6dd7681379e1c16ca545f0cc2dae0b5192474d852")
    version("1.7.1", sha256="ee331ba7b30f81d4afd5b9cea69023b0c4643c2f588352bdbd82b60c7d0082dc")
    version("1.7.0", sha256="780ed951a01be932b79d3d7ecb522b70ba25dd45b1a3cc0d984897d606856e8a")
    version("1.6.1", sha256="2935d46e977ae331ba6b4f547d5ee8624f3ebb7da79475861c450b5013e89d40")
    version("1.6.0", sha256="303f459b8482cf5b323b67f2784111c9d333b6e9b253f3f78319383966ef5303")
    version("1.5.5", sha256="67ff8210f08e9f2ee6ba23c8c26336f948420db5db7fc054c3a662e9017f18a3")
    version("1.5.4", sha256="4c53e932ba8d82616b65500f403a33a14957b9266b5e931e2448f1f005990750")

    depends_on("cmake@3.12:", type="build")
    depends_on("m4", type="build")

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )
