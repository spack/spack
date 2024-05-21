# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cppad(CMakePackage):
    """A Package for Differentiation of C++ Algorithms."""

    maintainers("whart222")

    homepage = "https://www.coin-or.org/CppAD/"
    url = "https://github.com/coin-or/CppAD/archive/refs/tags/20240000.4.tar.gz"
    git = "https://github.com/coin-or/CppAD.git"

    version("develop", branch="master")
    version(
        "20240000.4", sha256="0dfc1e30b32d5dd3086ee3adb6d2746a019e9d670b644c4d5ec1df3c35dd1fe5"
    )
    version(
        "20220000.5", sha256="9fb4562f6169855eadcd86ac4671593d1c0edf97bb6ce7cbb28e19af2bfc165e"
    )
    version(
        "20180000.0", sha256="1c355713e720fc5226ff3d6db2909922d46cd7ee0d36ee7985882f86905f655a"
    )
    version("20170114", sha256="fa3980a882be2a668a7522146273a1b4f1d8dabe66ad4aafa8964c8c1fd6f957")

    def cmake_args(self):
        args = [
            self.define("cppad_prefix", self.prefix),
            # self.define("cmake_install_docdir", "share/cppad/doc"),
        ]
        # This package does not obey CMAKE_INSTALL_PREFIX
        # args.append("-DCMAKE_INSTALL_PREFIX=%s" % self.prefix)

        args.append("-DCMAKE_BUILD_TYPE=Release")

        return args
