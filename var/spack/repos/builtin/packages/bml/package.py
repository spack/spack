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
    version("2.2.0", sha256="80d66a200fe05f3de9d531dda719ac9aafa446d5")
    version("2.1.2", sha256="ebe1c3840c4321991cb93d16ad28c4d5e3b66653")
    version("2.1.1", sha256="7c4e692b0a1d435eb6bfd65f9b5433ec369de102")
    version("2.1.0", sha256="782f514488cff1f305c6e66896d5fd4b9db39c8b")
    version("2.0.1", sha256="6ec98946846837a7639a09ba3a54a92f4212efdc")
    version("2.0.0", sha256="190ee052638e9253f2627b03cd8732dcb5c583cb")
    version("1.3.1", sha256="17145eda96aa5e550dcbff1ee7ce62b45723af8210b1ab70c5975ec792fa3d13")
    version("1.3.0", sha256="d9465079fe77210eb2af2dcf8ed96802edf5bb76bfbfdbcc97e206c8cd460b07")
    version("1.2.3", sha256="9a2ee6c47d2445bfdb34495497ea338a047e9e4767802af47614d9ff94b0c523")
    version("1.2.2", sha256="89ab78f9fe8395fe019cc0495a1d7b69875b5708069faeb831ddb9a6a9280a8a")
    version("1.1.0", sha256="29162f1f7355ad28b44d3358206ccd3c7ac7794ee13788483abcbd2f8063e7fc")

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
