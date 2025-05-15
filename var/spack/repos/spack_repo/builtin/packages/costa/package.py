# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Costa(CMakePackage):
    """
    Distributed Communication-Optimal Matrix Transpose and Reshuffle Library
    Based on the paper: https://arxiv.org/abs/2106.06601
    """

    maintainers("haampie", "kabicm", "RMeli", "mtaillefumier")
    homepage = "https://github.com/eth-cscs/COSTA"
    url = "https://github.com/eth-cscs/COSTA/archive/refs/tags/v2.2.4.tar.gz"
    git = "https://github.com/eth-cscs/COSTA.git"
    list_url = "https://github.com/eth-cscs/COSTA/releases"

    license("BSD-3-Clause")

    # note: The default archives produced with github do not have the archives
    #       of the submodules.
    version("master", branch="master", submodules=True)
    version("2.2.4", sha256="2155af3696cd0db1d18f9da7325de6fbcd87833c5b9e62445229e17151f7fd0b")
    version("2.2.3", sha256="e0b74851603b9da1a104dfaf50504c8af748c73999610a37f9384ed0c23ae5df")
    version("2.2.2", sha256="e87bc37aad14ac0c5922237be5d5390145c9ac6aef0350ed17d86cb2d994e67c")
    version("2.2.1", sha256="aa8aa2a4a79de094f857c22293825de270ff72becd6bd736ff9f2dd8c192446d")
    version("2.2", sha256="3e7333f012af76ec3508276ea90800313f6136504667021fe229e710bf6acdc7")
    version("2.1", sha256="c1e86452415083f7470b292d93ec60708b7c8dbafc2bac383636bb4b28135866")
    version("2.0", sha256="de250197f31f7d23226c6956a687c3ff46fb0ff6c621a932428236c3f7925fe4")

    variant("scalapack", default=False, description="Build with ScaLAPACK API")
    variant("shared", default=True, description="Build shared libraries")
    variant("profiling", default=False, description="Enable profiling")
    variant("tests", default=False, description="Enable tests")
    variant("apps", default=False, description="Enable miniapp")
    variant("benchmarks", default=False, description="Enable benchmarks")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.22:", type="build")
    depends_on("mpi@3:")
    depends_on("scalapack", when="+scalapack")
    depends_on("cxxopts", when="+apps")
    depends_on("cxxopts", when="+tests")
    depends_on("semiprof", when="+profiling")

    def url_for_version(self, version):
        if version == Version("2.0"):
            return "https://github.com/eth-cscs/COSTA/releases/download/v{0}/COSTA-v{1}.tar.gz".format(
                version, version
            )
        return "https://github.com/eth-cscs/COSTA/archive/refs/tags/v{0}.tar.gz".format(version)

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        return

    def costa_scalapack_cmake_arg(self):
        spec = self.spec

        if spec.satisfies("~scalapack"):
            return "OFF"
        elif spec.satisfies("^[virtuals=scalapack] intel-oneapi-mkl"):
            return "MKL"
        elif spec.satisfies("^[virtuals=scalapack] cray-libsci"):
            return "CRAY_LIBSCI"

        return "CUSTOM"

    def cmake_args(self):
        return [
            self.define_from_variant("COSTA_WITH_BENCHMARKS", "benchmarks"),
            self.define_from_variant("COSTA_WITH_APPS", "apps"),
            self.define_from_variant("COSTA_WITH_TESTS", "tests"),
            self.define_from_variant("COSTA_WITH_PROFILING", "profiling"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("COSTA_SCALAPACK", self.costa_scalapack_cmake_arg()),
        ]
