# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sol2(CMakePackage):
    """A fast, simple C++ and Lua Binding"""

    homepage = "https://sol2.rtfd.io"
    git = "https://github.com/ThePhD/sol2.git"

    maintainers("rbberger")

    license("MIT")

    version("develop", branch="develop")
    version("3.3.0", tag="v3.3.0", commit="eba86625b707e3c8c99bbfc4624e51f42dc9e561")

    depends_on("lua")

    def cmake_args(self):
        args = [
            self.define("SOL2_BUILD_LUA", False),
            self.define("SOL2_LUA_VERSION", self.spec["lua"].version),
        ]
        return args
