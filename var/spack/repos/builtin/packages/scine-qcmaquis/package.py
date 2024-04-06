# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ScineQcmaquis(CMakePackage):
    """Scine QCMaquis DMRG Solver"""

    homepage = "https://scine.ethz.ch/download/qcmaquis"
    git = "https://github.com/qcscine/qcmaquis.git"

    maintainers("adam-grofe")

    version("master", branch="master")
    version("3.1.3", branch="release-3.1.3")
    version("3.1.2", branch="release-3.1.2", preferred=True)
    variant(
        "blas",
        values=("openblas", "mkl"),
        default="openblas",
        description="Which blas library to use.",
    )
    variant(
        "symmetries",
        default="SU2U1PG,TwoU1PG",
        description='Wave functions symmetries to compile (e.g. "SU2U1PG,TwoU1PG")',
        values=("U1", "TwoU1", "TwoU1PG", "NU1", "Z2", "SU2U1", "SU2U1PG", "U1DG", "NONE"),
        multi=True,
    )
    variant(
        "build_tests",
        default=True,
        description="Whether to build unit tests using gtest and gmock",
    )

    root_cmakelists_dir = "dmrg"

    depends_on("hdf5~mpi")
    depends_on("lapack")
    depends_on("openblas+ilp64 threads=openmp", when="blas=openblas")
    depends_on("intel-oneapi-mkl", when="blas=mkl")
    depends_on("gsl")
    depends_on("boost+program_options+filesystem+system+thread+serialization+chrono")
    depends_on("googletest+gmock", when="+build_tests")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SYMMETRIES", "symmetries"),
            self.define_from_variant("QCMAQUIS_TESTS", "build_tests"),
        ]
        return args

    def patch(self):
        if self.version <= Version("3.1.3"):
            filter_file(
                "#include <vector>",
                "#include <vector>\n#include <map>",
                "dmrg/framework/dmrg/utils/results_collector.h",
            )
