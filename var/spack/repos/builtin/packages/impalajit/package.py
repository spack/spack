# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Impalajit(CMakePackage):
    """A lightweight JIT compiler for flexible data access in simulation applications."""

    homepage = "https://github.com/manuel-fasching/ImpalaJIT/blob/master/README.md"
    version("develop", git="https://github.com/manuel-fasching/ImpalaJIT.git", branch="master")
    maintainers = ["Thomas-Ulrich", "ravil-mobile"]
    variant("static", default=True, description="compile as a static lib")
    depends_on("cmake", type="build")
    depends_on("pkg-config", type="build")

    def cmake_args(self):
        args = []
        args.append(self.define("STATIC_LIB", "+static" in self.spec))
        args.append(self.define("SHARED_LIB", "~static" in self.spec))
        args.append(self.define("TESTS", self.run_tests))

        if self.compiler != "intel":
            args.append("-DINTEL_COMPILER=OFF")

        return args
