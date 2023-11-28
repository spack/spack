# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cdt(CMakePackage):
    """CDT is a C++ library for generating constraint or conforming Delaunay triangulations."""

    homepage = "https://artem-ogre.github.io/CDT"
    url = "https://github.com/artem-ogre/CDT/archive/refs/tags/1.3.0.tar.gz"

    maintainers("jcortial-safran")

    version("1.3.0", sha256="7e8feadf9534cf79f9bf188365510fd6bc68ea997758e1c68d1569f98da924da")

    variant(
        "boost",
        default=False,
        description="Use Boost as a fallback for features missing in C++98 and performance tweaks",
    )
    variant(
        "64_bit_index",
        default=False,
        description="Use 64bits to store vertex/triangle index types. Otherwise 32bits are used.",
    )
    variant(
        "compiled",
        default=False,
        description="Instantiate templates for float and double and compiled into a library",
    )
    variant("shared", default=True, description="Compile as a shared library")

    depends_on("cmake@3.4:", type="build")
    depends_on("boost", when="+boost")

    root_cmakelists_dir = "CDT"

    def cmake_args(self):
        return [
            self.define_from_variant("CDT_USE_BOOST", "boost"),
            self.define_from_variant("CDT_USE_64_BIT_INDEX_TYPE", "64_bit_index"),
            self.define_from_variant("CDT_USE_AS_COMPILED_LIBRARY", "compiled"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]
