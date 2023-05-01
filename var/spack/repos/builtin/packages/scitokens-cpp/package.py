# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ScitokensCpp(CMakePackage):
    """A C++ implementation of the SciTokens library with a C library interface.
    SciTokens provide a token format for distributed authorization."""

    homepage = "https://github.com/scitokens/scitokens-cpp"
    url = "https://github.com/scitokens/scitokens-cpp/archive/refs/tags/v0.7.0.tar.gz"

    version("1.0.0", sha256="88376c5cd065aac8d92445184a02ccf5186dc4890ccd7518e88be436978675c0")
    version("0.7.1", sha256="44a1bca188897b1e97645149d1f6bc187cd0e482ad36159ca376834f028ce5ef")
    version("0.7.0", sha256="72600cf32523b115ec7abf4ac33fa369e0a655b3d3b390e1f68363e6c4e961b6")

    depends_on("cmake@2.6:")
    depends_on("cmake@3.10:", when="@0.7.1:")
    depends_on("openssl")
    depends_on("sqlite")
    depends_on("curl")
    depends_on("pkgconfig", type="build")
    depends_on("uuid", type="build")

    # https://github.com/scitokens/scitokens-cpp/issues/72
    @when("@0.7.0 ^openssl@3:")
    def patch(self):
        filter_file(" -Werror", "", "CMakeLists.txt")
