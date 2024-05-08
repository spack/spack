# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsonata(CMakePackage):
    """
    `libsonata` provides C++ API for reading SONATA Nodes / Edges

    See also:
    https://github.com/AllenInstitute/sonata/blob/master/docs/SONATA_DEVELOPER_GUIDE.md
    """

    homepage = "https://github.com/BlueBrain/libsonata"
    git = "https://github.com/BlueBrain/libsonata.git"
    url = "https://pypi.io/packages/source/l/libsonata/libsonata-0.1.14.tar.gz"

    version("develop", branch="master", get_full_repo=True)
    version("0.1.26", tag="v0.1.26")
    version("0.1.25", tag="v0.1.25")
    version("0.1.24.1", commit="0577eb5142e65363087facb9dc6c12dfd2ae49f2")
    version("0.1.24", tag="v0.1.24")
    version("0.1.23", tag="v0.1.23")
    version("0.1.22", tag="v0.1.22")
    version("0.1.21", tag="v0.1.21")
    version("0.1.20", tag="v0.1.20")
    version("0.1.18", tag="v0.1.18")
    version("0.1.17", tag="v0.1.17")
    version("0.1.16", tag="v0.1.16")
    version("0.1.15", tag="v0.1.15")
    version("0.1.14", tag="v0.1.14")
    version("0.1.13", tag="v0.1.13")
    version("0.1.12", tag="v0.1.12")
    version("0.1.11", tag="v0.1.11")
    version("0.1.10", tag="v0.1.10")

    # This was added to be able to build nmodl with catch2@3
    # TODO: remove in the next version
    patch("0001-Include-Catch2-only-if-building-tests.patch", when="@:0.1.20")

    variant("mpi", default=True, description="Enable MPI backend")
    variant("tests", default=False, description="Enable building tests")
    variant("cxxstd", default="14", when="@0.1.17:", description="The C++ standard to use")

    depends_on("cmake@3.3:", type="build")
    depends_on("py-setuptools-scm", type="build", when="@0.1:")
    depends_on("fmt@4.0:")
    depends_on("highfive+mpi", when="+mpi")
    depends_on("highfive~mpi", when="~mpi")
    depends_on("mpi", when="+mpi")
    depends_on("catch2@2", when="@0.1.3: +tests")
    # Version restriction guessed from old deployment
    #
    # No `when` clause, as clingo will penalize new versions with the
    # version penalty from `nlohmann-js` then :(
    depends_on("nlohmann-json@:3.9.1")

    conflicts("^highfive@2.5:2.6")

    def cmake_args(self):
        result = [
            "-DEXTLIB_FROM_SUBMODULES=OFF",
            self.define_from_variant("SONATA_TESTS", "tests"),
        ]

        if self.spec.satisfies("@0.1.17:"):
            result.append(self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"))

        if not self.spec.satisfies("@develop"):
            result.append("-DSONATA_CXX_WARNINGS:BOOL=OFF")
        if self.spec.satisfies("+mpi"):
            result.extend(
                [
                    "-DCMAKE_C_COMPILER:STRING={0}".format(self.spec["mpi"].mpicc),
                    "-DCMAKE_CXX_COMPILER:STRING={0}".format(self.spec["mpi"].mpicxx),
                ]
            )
        return result
