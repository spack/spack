# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Discotec(SConsPackage):
    """This project contains DisCoTec, a code for the distributed sparse
    grid combination technique with MPI parallelization."""

    homepage = "https://github.com/SGpp/DisCoTec"
    url = "https://github.com/SGpp/DisCoTec"
    git = "https://github.com/SGpp/DisCoTec"

    # notify when the package is updated.
    maintainers = ["freifrauvonbleifrei", "pfluegdk"]

    version("master", branch="master")
    version("third-level-advection", branch="third-level-advection")

    variant("enableft", default=False, description="DisCoTec with algorithm-based fault tolerance")
    variant("gene", default=False, description="Build for GENE (as task library)")
    variant("timing", default=True, description="With high-res timers")
    variant("test", default=True, description="Build Boost tests")
    variant("openmp", default=False, description="Parallelize with OpenMP")
    variant("hdf5", default=True, description="Interpolation output with HDF5")
    variant("debug", default=False, description="Build with assertions and debug symbols")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("scons", type=("build"))
    depends_on("mpi", type=("build", "run"))
    depends_on("boost +test +serialization", type=("build", "run"))
    depends_on("highfive+mpi", when="+hdf5")

    def build_args(self, spec, prefix):
        # Testing parameters
        if "+test" in spec:
            self.args = ["COMPILE_BOOST_TESTS=1", "RUN_BOOST_TESTS=0"]
        else:
            self.args = ["COMPILE_BOOST_TESTS=0", "RUN_BOOST_TESTS=0"]
        # I apologize for quite a lot of not-useful flags
        self.args.append("VERBOSE=1")
        self.args.append("UNIFORMDECOMPOSITION=1")
        self.args.append("DEBUG_OUTPUT=0")
        self.args.append("DOC=0")
        self.args.append("RUN_CPPLINT=0")
        self.args.append("BUILD_STATICLIB=0")
        self.args.append("CPPFLAGS=")
        self.args.append("LINKFLAGS=")

        self.args.append("TIMING={0}".format("1" if "+test" in spec else "0"))
        self.args.append("OPT={0}".format("0" if "+debug" in spec else "1"))
        self.args.append("ENABLEFT={0}".format("1" if "+enableft" in spec else "0"))
        self.args.append("USE_HDF5={0}".format("1" if "+hdf5" in spec else "0"))

        # Get the mpicxx compiler from the Spack spec
        # (makes certain we use the one from spack):
        self.args.append("CXX={0}".format(self.spec["mpi"].mpicxx))
        self.args.append("CC={0}".format(self.spec["mpi"].mpicc))
        self.args.append("FC=")

        if "+openmp" in spec:
            self.args.append("CPPFLAGS={0}".format(self.spec["mpi"].mpicxx.openmp_flag))
        return self.args

    def install(self, pkg, spec):
        """does nothing"""
        pass
