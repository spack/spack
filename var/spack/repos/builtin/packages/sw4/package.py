# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *

class Sw4(MakefilePackage):
    """This package builds SW4 with HDF5, PROJ, and ZFP."""

    homepage = "https://github.com/geodynamics/sw4"
    git = "https://github.com/geodynamics/sw4.git"

    maintainers = ["houjun", "andersp"]

    # tags = ["e4s"]

    version("3.0-beta", tag="v3.0-beta")
    version("developer", branch="developer")
    version("master", branch="master")

    depends_on("mpi")
    depends_on("proj")
    depends_on("blas")
    depends_on("lapack")
    depends_on("hdf5+mpi")
    depends_on("zfp")
    depends_on("fftw@3.0: +mpi")
    depends_on("h5z-zfp")

    def edit(self, spec, prefix):
        os.environ["CXX"] = spec["mpi"].mpicc
        os.environ["FC"] = spec["mpi"].mpifc
        os.environ["proj"] = "yes"
        os.environ["SW4ROOT"] = self.spec["proj"].prefix
        os.environ["hdf5"] = "yes"
        os.environ["HDF5ROOT"] = self.spec["hdf5"].prefix
        os.environ["zfp"] = "yes"
        os.environ["H5ZROOT"] = self.spec["h5z-zfp"].prefix
        os.environ["ZFPROOT"] = self.spec["zfp"].prefix
        os.environ["fftw"] = "yes"
        os.environ["FFTWHOME"] = self.spec["fftw"].prefix
        os.environ["EXTRA_CXX_FLAGS"] = " -I" + self.spec["blas"].prefix + "/include"
        os.environ["EXTRA_LINK_FLAGS"] = "-lstdc++ -lm -ldl -lopenblas" + " -L" + self.spec["blas"].prefix + "/lib"

        if "%gcc" in self.spec:
            os.environ["EXTRA_LINK_FLAGS"] += " -lgfortran"
    
    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("optimize_mp/sw4", prefix.bin)
        install_tree("pytest", prefix.test)

