# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Elsi(CMakePackage):
    """ELSI provides a unified interface for electronic structure
    codes to a variety of eigenvalue solvers."""

    homepage = "https://wordpress.elsi-interchange.org/"
    url      = "http://wordpress.elsi-interchange.org/wp-content/uploads/2019/03/elsi-2.2.1.tar.gz"

    version('2.2.1', sha256='5b4b2e8fa4b3b68131fe02cc1803a884039b89a1b1138af474af66453bec0b4d')

    variant(
      'enable_pexsi', default=False, description='Enable PEXSI support'
    )
    variant(
      'enable_sips', default=False, description='Enable SLEPc-SIPs support'
    )

    depends_on('blas')
    depends_on('cmake')
    depends_on('elpa')
    depends_on('lapack')
    depends_on('mpi')
    depends_on('ntpoly')
    depends_on('slepc', when='+enable_sips')
    depends_on('petsc', when='+enable_sips')
    depends_on('scalapack')
    depends_on('superlu', when='+enable_pexsi')

    def cmake_args(self):
        args = []

        # Compiler Information
        # (ELSI wants these explicitly set)
        args += ["-DCMAKE_Fortran_COMPILER="+self.spec["mpi"].mpifc]
        args += ["-DCMAKE_C_COMPILER="+self.spec["mpi"].mpicc]
        args += ["-DCMAKE_CXX_COMPILER="+self.spec["mpi"].mpicxx]

        # External Arguments
        #args += ["-DUSE_EXTERNAL_ELPA=ON"]
        args += ["-DUSE_EXTERNAL_NTPOLY=ON"]

        # Optional parameters
        if '+enable_pexsi' in self.spec:
            args += ["-DENABLE_PEXSI=ON"]
            args += ["-DUSE_EXTERNAL_SUPERLU=ON"]
        if '+enable_sips' in self.spec:
            args += ["-DENABLE_SIPS=ON"]

        return args
