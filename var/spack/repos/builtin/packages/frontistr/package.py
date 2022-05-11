# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.util.package import *


class FrontistrBase(CMakePackage):
    """Base class for building Frontistr, shared with the Fujitsu optimized version
    of the package in the 'fujitsu-frontistr' package."""

    variant('build_type', default='RELEASE',
            description='CMake build type',
            values=('DEBUG', 'RELEASE'))

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack')
    depends_on('revocap-refiner')
    # depends_on('revocap-coupler')
    depends_on('metis')
    depends_on('mumps')
    depends_on('trilinos@:12.18.1')

    def cmake_args(self):
        define = CMakePackage.define
        cmake_args = [
            define('WITH_ML', True),
            define('REFINER_INCLUDE_PATH',
                   self.spec['revocap-refiner'].prefix.include),
            define('REFINER_LIBRARIES',
                   join_path(self.spec['revocap-refiner'].prefix.lib,
                             'libRcapRefiner.a'))
        ]
        return cmake_args


class Frontistr(FrontistrBase):
    """Open-Source Large-Scale Parallel FEM Program for
        Nonlinear Structural Analysis"""

    homepage = "https://www.frontistr.com/"
    git      = "https://gitlab.com/FrontISTR-Commons/FrontISTR.git"
    maintainers = ['hiroshi.okuda', 'kgoto', 'morita', 'inagaki', 'michioga']

    version('5.3', tag='v5.3')
    version('5.2', tag='v5.2')
    version('5.1.1', tag='v5.1.1')
    version('5.1', tag='v5.1')
    version('5.0', tag='v5.0')
    version('master', tag='master')
