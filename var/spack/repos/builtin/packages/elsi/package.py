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

    depends_on('cmake')
    depends_on('mpi')
    depends_on('slepc')
    depends_on('petsc')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack')
    depends_on('elpa')
    depends_on('ntpoly')
    depends_on('superlu')

    def cmake_args(self):
        args = []
        args += "-DUSE_EXTERNAL_ELPA=ON"
        args += "-DUSE_EXTERNAL_NTPOLY=ON"
        args += "-DUSE_EXTERNAL_SUPERLU=ON"
        return args
