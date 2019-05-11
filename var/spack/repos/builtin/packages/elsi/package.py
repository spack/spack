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

    # Variants
    variant(
      'enable_pexsi', default=False, description='Enable PEXSI support'
    )
    variant(
      'enable_sips', default=False, description='Enable SLEPc-SIPs support'
    )
    variant(
      'external_elpa', default=True, description="Build ELPA using SPACK"
    )
    variant(
      'external_ntpoly', default=True, description="Build NTPoly using SPACK"
    )

    # Basic dependencies
    depends_on('blas', type="link")
    depends_on('lapack', type="link")
    depends_on('cmake', type="build")
    depends_on('mpi')
    depends_on('scalapack', type="link")

    # Library dependencies
    depends_on('elpa', when='+external_elpa')
    depends_on('ntpoly', when='+external_ntpoly')
    depends_on('slepc', when='+enable_sips')
    depends_on('petsc', when='+enable_sips')
    depends_on('superlu-dist', when='+enable_pexsi')

    def cmake_args(self):
        from os.path import dirname

        args = []

        # Compiler Information
        # (ELSI wants these explicitly set)
        args += ["-DCMAKE_Fortran_COMPILER="+self.spec["mpi"].mpifc]
        args += ["-DCMAKE_C_COMPILER="+self.spec["mpi"].mpicc]
        args += ["-DCMAKE_CXX_COMPILER="+self.spec["mpi"].mpicxx]

        # External Arguments
        if '+external_elpa' in self.spec:
            args += ["-DUSE_EXTERNAL_ELPA=ON"]

            # Setup the searchpath for elpa
            elpa = self.spec['elpa']
            elpa_module = find(elpa.prefix, 'elpa.mod')
            args += ["-DINC_PATHS="+dirname(elpa_module[0])]

        if '+external_ntpoly' in self.spec:
            args += ["-DUSE_EXTERNAL_NTPOLY=ON"]
        
        if '+enable_pexsi' in self.spec:
            args += ["-DENABLE_PEXSI=ON"]
            args += ["-DUSE_EXTERNAL_SUPERLU=ON"]
        if '+enable_sips' in self.spec:
            args += ["-DENABLE_SIPS=ON"]

        return args
