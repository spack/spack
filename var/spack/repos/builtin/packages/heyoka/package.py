# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Heyoka(CMakePackage):
    """heyoka is a C++ library for integration of ODEs via Taylor’s method"""

    homepage = "https://bluescarni.github.io/heyoka"
    url = "https://github.com/bluescarni/heyoka/archive/refs/tags/v3.2.0.tar.gz"

    # A list of GitHub accounts to notify when the package is updated.
    maintainers("bluescarni", "agseaton")

    # SPDX identifier of the project's license.
    license("MPL-2.0")

    version("3.2.0", sha256="37db24fbaf0e65d740ffb20f76ac1c8ab9fbd6893dc87dfd483c965b71dbf465")
    version("3.1.0", sha256="7eecab47f44a9fff022cf24f226763dab8b075a9fdaa543a42f64bb2634b3ad8")
    version("3.0.0", sha256="03ccb6fb015ad43877781763c0f2f49bd6db64c8b9493174e589c970ef00d7f2")
    version("2.0.0", sha256="418ce55557496d3ff1383e8b64663661d9b6a5f39dc7080e401d6537db0c4cd2")
    version("1.0.0", sha256="96f2e049e0518c49dbe224fc268ab1ad80abeaa306e2fe7a30e2acffb79c04af")
    version("0.21.0", sha256="16d22e99397139d25b2a0c418a654e9cba3684c7eb28933791526bb163f50f27")
    version("0.20.1", sha256="7abd68d319dd2740ca8440d41602ceefb45809d6fadbbf31728c5cb003511f8c")
    version("0.20.0", sha256="d6b4601ee28fc2dbb84c317bbe2619c776ce448f782c045a801dfa46b0d5e52c")
    version("0.19.0", sha256="7a7634379233be778fd6b15090df287787cc429314ec521d0336cdc1ae26642a")
    version("0.18.0", sha256="2a14a988d973d9a76424df05d38f89ae64f7a1e1c12131022e338fe2de2dcb94")

    # Define variants of the package
    variant("mppp", default=False, description="enable features relying on the mp++ library")
    variant("sleef", default=False, description="enable features relying on the SLEEF library")
    variant("tests", default=False, description="build the test suite")
    variant("benchmarks", default=False, description="build the benchmarking suite")
    variant("tutorials", default=False, description="build the tutorials")
    variant(
        "static",
        default=False,
        description=("build heyoka as a static library, instead of a dynamic library"),
    )

    # Dependencies

    # Build dependencies
    depends_on("cmake@3.18:", type="build")

    # Required dependencies
    depends_on("llvm@13:17")
    depends_on("boost@1.69: +serialization")
    depends_on("fmt@9:10")
    depends_on("spdlog")
    depends_on("intel-tbb@2021.4.0:")

    # Optional dependencies
    depends_on("boost@1.69: +serialization +program_options", when="+benchmarks")
    depends_on("mppp@1 +serialization +fmt +mpfr +mpc", when="+mppp")
    depends_on("sleef", when="+sleef")
    depends_on("xtensor", when="+benchmarks")
    depends_on("xtensor-blas", when="+benchmarks")
    depends_on("xtensor", when="+tests")
    depends_on("xtensor-blas", when="+tests")

    def cmake_args(self):
        args = [
            self.define_from_variant("HEYOKA_WITH_MPPP", "mppp"),
            self.define_from_variant("HEYOKA_WITH_SLEEF", "sleef"),
            self.define_from_variant("HEYOKA_BUILD_TESTS", "tests"),
            self.define_from_variant("HEYOKA_BUILD_BENCHMARKS", "benchmarks"),
            self.define_from_variant("HEYOKA_BUILD_TUTORIALS", "tutorials"),
            self.define_from_variant("HEYOKA_BUILD_STATIC_LIBRARY", "static"),
            self.define_from_variant("HEYOKA_ENABLE_IPO", "ipo"),
        ]
        return args
