# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Trilinos(Package):
    """A package which has pure build dependencies, run dependencies, and link dependencies."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/trilinos-1.0.tar.gz"

    version("16.1.0", md5="00000000000000000000000000000120")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake", type="build")

    depends_on("py-numpy", type="run")

    depends_on("mpi")
    depends_on("callpath")

    # The variant default value cannot be taken by the default version of the package
    variant("disable17", default=False, description="Disable support for C++17")
    variant(
        "cxxstd",
        default="14",
        description="C++ standard",
        values=["14", "17", "20", "23"],
        multi=False,
    )
    conflicts("cxxstd=14", when="@16:")
    conflicts("cxxstd=17", when="+disable17")
