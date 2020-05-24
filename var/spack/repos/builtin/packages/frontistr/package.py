# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Frontistr(CMakePackage):
    """Open-Source Large-Scale Parallel FEM Program for
        Nonlinear Structural Analysis"""

    homepage = "https://github.com/FrontISTR/FrontISTR"
    git      = "https://github.com/FrontISTR/FrontISTR.git"

    version('5.0', tag='v5.0')

    depends_on('mpi')
    depends_on('revocap-refiner')
    depends_on('revocap-coupler')
    depends_on('blas')
    depends_on('metis')
    depends_on('scalapack')
    depends_on('mumps +mpi')
    depends_on('trilinos')

    def cmake_args(self):
        define = CMakePackage.define
        cmake_args = [
            define('WITH_ML', True),
        ]
        return cmake_args
