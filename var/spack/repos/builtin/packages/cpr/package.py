# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cpr(CMakePackage):
    """C++ Requests: Curl for People, a spiritual port of Python Requests."""

    homepage = "https://docs.libcpr.org/"
    url = "https://github.com/libcpr/cpr/archive/refs/tags/1.10.4.tar.gz"

    maintainers("sethrj")

    version("1.10.4", sha256="88462d059cd3df22c4d39ae04483ed50dfd2c808b3effddb65ac3b9aa60b542d")
    version("1.9.2", sha256="3bfbffb22c51f322780d10d3ca8f79424190d7ac4b5ad6ad896de08dbd06bf31")

    depends_on("curl")
    depends_on("git", type="build")

    def cmake_args(self):
        _force = "_FORCE" if self.spec.satisfies("@:1.9") else ""

        return [
            self.define("CPR_USE_SYSTEM_GTEST", True),
            self.define(f"CPR{_force}_USE_SYSTEM_CURL", True),
            self.define("CPR_ENABLE_SSL", True),
        ]
