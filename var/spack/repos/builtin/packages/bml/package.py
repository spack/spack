# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bml(CMakePackage):
    """The basic matrix library (bml) is an implementation of various matrix data
    formats (dense and sparse) and their associated algorithms for basic
    matrix operations used in electronic structure solvers."""

    homepage = "https://lanl.github.io/bml/"
    url = "https://github.com/lanl/bml/tarball/v2.2.0"
    git = "https://github.com/lanl/bml.git"
    
    maintainers = ["jeanlucf22"]

    version("develop", branch="master")
    version("2.2.0", sha256="9a975072263e7f7b0189c2544dc824f936dd736c16760a5b5d2de6a638da854f")
    version("2.1.2", sha256="efbaa2ae4b555380e989049fb79ddc991bb1a1a1dec310d0332db143445baaec")
    version("2.1.1", sha256="03fa886a10a8c0f5dbab337717c03bf4f006523dfcad7263f44aeb4187e13a9d")
    version("2.1.0", sha256="ce0e2a52215b71bddcc919274d05a5cec5033e4a231acc33babbd656ee24cb48")
    version("2.0.1", sha256="a9f22725ad54af9c2f2241b079d1c6f3ed3dab710129209342bf86f54aa798fc")
    version("2.0.0", sha256="1ed2b9e9925b20989d3257da00440ded61dd8d9a5ee2e0802772bf08703f3a5c")
    version("1.3.1", sha256="17145eda96aa5e550dcbff1ee7ce62b45723af8210b1ab70c5975ec792fa3d13")
    version("1.3.0", sha256="d9465079fe77210eb2af2dcf8ed96802edf5bb76bfbfdbcc97e206c8cd460b07")

    variant("shared", default=True, description="Build shared libs")
    variant("mpi", default=True, description="Build with MPI Support")

    conflicts("+mpi", when="@:1.2.2")

    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi", when="+mpi")
    depends_on("python", type="build")

    def cmake_args(self):
        args = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]
        spec = self.spec
        if "+mpi" in spec:
            args.append("-DBML_MPI=True")
            args.append("-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc)
            args.append("-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx)
            args.append("-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc)
        else:
            args.append("-DBML_MPI=False")
        return args
