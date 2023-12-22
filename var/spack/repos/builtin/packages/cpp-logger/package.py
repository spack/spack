# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CppLogger(CMakePackage):
    """A simple C++ logger"""

    homepage = "https://github.com/hariharan-devarajan/cpp-logger"
    git = "https://github.com/hariharan-devarajan/cpp-logger.git"
    maintainers("hariharan-devarajan")

    version("develop", branch="develop")
    version("master", branch="master")
    version("0.0.1", tag="v0.0.1", commit="d48b38ab14477bb7c53f8189b8b4be2ea214c28a")
    version("0.0.2", tag="v0.0.2", commit="329a48401033d2d2a1f1196141763cab029220ae")
