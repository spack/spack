# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Discotec(CMakePackage):
    """This project contains DisCoTec, a code for the distributed sparse
    grid combination technique with MPI parallelization."""

    homepage = "https://github.com/SGpp/DisCoTec"
    url = "https://github.com/SGpp/DisCoTec"
    git = "https://github.com/SGpp/DisCoTec"

    # notify when the package is updated.
    maintainers = ["freifrauvonbleifrei", "pfluegdk"]

    version("main", branch="main")

    variant(
        "build_type",
        default="Release",
        values=("Release", "RelWithDebInfo", "Debug"),
        description="Build type for DisCoTec",
    )
    variant("enableft", default=False, description="DisCoTec with algorithm-based fault tolerance")
    variant("gene", default=False, description="Build for GENE (as task library)")
    variant("hdf5", default=True, description="Interpolation output with HDF5")
    variant("lto", default=True, description="Build with link-time optimization")
    variant("openmp", default=False, description="Parallelize with OpenMP")
    variant("timing", default=True, description="With high-res timers")
    variant("test", default=True, description="Build Boost tests")
    variant("selalib", default=False, description="Build selalib example")
    variant("vtk", default=False, description="Build with VTK support")

    depends_on(
        "boost +test +serialization +filesystem +system +program_options", type=("build", "run")
    )
    depends_on("cmake@3.24.2:", type=("build"))
    depends_on("glpk")
    depends_on("highfive+mpi+boost+ipo", when="+hdf5")
    depends_on("mpi", type=("build", "run"))
    depends_on("vtk", when="+vtk")

    def cmake_args(self):
        args = [
            "-DDISCOTEC_BUILD_MISSING_DEPS=OFF",
            "-DDISCOTEC_ENABLEFT={0}".format("ON" if "+enableft" in self.spec else "OFF"),
            "-DDISCOTEC_GENE={0}".format("ON" if "+gene" in self.spec else "OFF"),
            "-DDISCOTEC_OPENMP={0}".format("ON" if "+openmp" in self.spec else "OFF"),
            "-DDISCOTEC_TIMING={0}".format("ON" if "+timing" in self.spec else "OFF"),
            "-DDISCOTEC_TEST={0}".format("ON" if "+test" in self.spec else "OFF"),
            "-DDISCOTEC_USE_HDF5={0}".format("ON" if "+hdf5" in self.spec else "OFF"),
            "-DDISCOTEC_USE_HIGHFIVE={0}".format("ON" if "+hdf5" in self.spec else "OFF"),
            "-DDISCOTEC_USE_LTO={0}".format("ON" if "+lto" in self.spec else "OFF"),
            "-DDISCOTEC_USE_VTK={0}".format("ON" if "+vtk" in self.spec else "OFF"),
            "-DDISCOTEC_WITH_SELALIB={0}".format("ON" if "+selalib" in self.spec else "OFF")
        ]

        return args
