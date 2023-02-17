# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Costa(CMakePackage):
    """
    Distributed Communication-Optimal Matrix Transpose and Reshuffle Library
    Based on the paper: https://arxiv.org/abs/2106.06601
    """

    maintainers("haampie", "kabicm", "RMeli")
    homepage = "https://github.com/eth-cscs/COSTA"
    git = "https://github.com/eth-cscs/COSTA.git"

    # note: The default archives produced with github do not have the archives
    #       of the submodules.
    version("master", branch="master", submodules=True)
    version("2.1", sha256="c1e86452415083f7470b292d93ec60708b7c8dbafc2bac383636bb4b28135866")
    version("2.0", sha256="de250197f31f7d23226c6956a687c3ff46fb0ff6c621a932428236c3f7925fe4")

    variant("scalapack", default=False, description="Build with ScaLAPACK API")
    variant("shared", default=False, description="Build shared libraries")

    depends_on("cmake@3.12:", type="build")
    depends_on("mpi@3:")
    depends_on("scalapack", when="+scalapack")

    def url_for_version(self, version):
        if version == Version("2.0"):
            return "https://github.com/eth-cscs/COSTA/releases/download/v{0}/COSTA-v{1}.tar.gz".format(
                version, version
            )
        else:
            return "https://github.com/eth-cscs/COSTA/archive/refs/tags/v{0}.tar.gz".format(
                version
            )

    def setup_build_environment(self, env):
        return

    def costa_scalapack_cmake_arg(self):
        spec = self.spec

        if "~scalapack" in spec:
            return "OFF"
        elif "^intel-mkl" in spec or "^intel-oneapi-mkl" in spec:
            return "MKL"
        elif "^cray-libsci" in spec:
            return "CRAY_LIBSCI"

        return "CUSTOM"

    def cmake_args(self):
        return [
            self.define("COSTA_WITH_BENCHMARKS", "OFF"),
            self.define("COSTA_WITH_APPS", "OFF"),
            self.define("COSTA_WITH_TESTS", "OFF"),
            self.define("COSTA_WITH_PROFILING", "OFF"),
            self.define("COSTA_SCALAPACK", self.costa_scalapack_cmake_arg()),
            self.define("BUILD_SHARED_LIBS", "+shared" in self.spec),
        ]
