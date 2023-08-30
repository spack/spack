# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ScineQcmaquis(CMakePackage):
    """Scine QCMaquis DMRG Solver"""

    homepage = "https://scine.ethz.ch/download/qcmaquis"
    git = "https://github.com/qcscine/qcmaquis.git"

    version("master", branch="master")
    version("3.1.3", branch="release-3.1.3")
    version("3.1.2", branch="release-3.1.2")
    variant(
        "blas",
        values=("openblas", "mkl"),
        default="openblas",
        description="Which blas library to use.",
    )
    variant(
        "symmetries",
        default="TwoU1;SU2U1;SU2U1PG;TwoU1PG",
        description='Which wave functions symmetries to compile (e.g. "TwoU1;SU2U1;SU2U1PG;TwoU1PG")',
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
    depends_on("boost+program_options+filesystem+system+thread+serialization")
    depends_on("googletest+gmock", when="build_tests=True")

    def cmake_args(self):
        args = []
        build_symm = str(self.spec.variants["symmetries"].value)
        if build_symm:
            args.extend(["-DBUILD_SYMMETRIES={}".format(build_symm)])
        build_tests = str(self.spec.variants["build_tests"].value)
        if build_tests:
            args.extend(["-DQCMAQUIS_TESTS=On"])
        return args

    def patch(self):
        if self.version <= Version("3.1.2"):
            filter_file(
                "#include <vector>",
                "#include <vector>\n#include <map>",
                "dmrg/framework/dmrg/utils/results_collector.h",
            )
