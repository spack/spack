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

    depends_on("curl")

    def cmake_args(self):
        args = [
            self.define("CPR_USE_SYSTEM_GTEST", True),
            self.define("CPR_USE_SYSTEM_CURL", True),
            self.define("CPR_ENABLE_SSL", True),
        ]
        return args
