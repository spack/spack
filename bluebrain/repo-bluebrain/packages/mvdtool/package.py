# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mvdtool(CMakePackage):
    """Reader library and tool for neuroscientific node formats (MVD, Sonata).
    For the Python bindings please see py-mvdtool
    """

    homepage = "https://github.com/BlueBrain/MVDTool"
    url = "https://github.com/BlueBrain/MVDTool.git"
    git = "https://github.com/BlueBrain/MVDTool.git"

    submodules = True

    version("develop", branch="master")
    version("2.4.9", tag="v2.4.9")

    variant("mpi", default=True, description="Enable MPI backend")

    depends_on("cmake@3.11:", type="build")

    depends_on("py-setuptools", type="build", when="@:2.1")

    # unit tests use Boost (test, filesystem)
    depends_on("boost+filesystem+test")
    depends_on("mpi", when="+mpi")
    depends_on("hdf5+mpi", when="+mpi")
    depends_on("hdf5~mpi", when="~mpi")
    depends_on("libsonata+mpi", when="+mpi")
    depends_on("libsonata~mpi", when="~mpi")
    depends_on("highfive+mpi", when="+mpi")
    depends_on("highfive~mpi", when="~mpi")

    def patch(self):
        filter_file("(EXTLIB_FROM_SUBMODULES)=ON", r"\1=OFF", "setup.py")

    def cmake_args(self):
        args = []
        if self.spec.satisfies("+mpi"):
            args.extend(
                [
                    "-DCMAKE_C_COMPILER:STRING={0}".format(self.spec["mpi"].mpicc),
                    "-DCMAKE_CXX_COMPILER:STRING={0}".format(self.spec["mpi"].mpicxx),
                ]
            )
        return args
