# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class DamaskMesh(CMakePackage):
    """Mesh solver for DAMASK"""

    homepage = "https://damask.mpie.de"
    url      = "https://damask.mpie.de/download/damask-3.0.0.tar.xz"

    maintainers = ['MarDiehl']

    version('3.0.0-alpha6', sha256='de6748c285558dec8f730c4301bfa56b4078c130ff80e3095faf76202f8d2109')
    version('3.0.0-alpha5', sha256='2d2b10901959c26a5bb5c52327cdafc7943bc1b36b77b515b0371221703249ae')
    version('3.0.0-alpha4', sha256='0bb8bde43b27d852b1fb6e359a7157354544557ad83d87987b03f5d629ce5493')

    depends_on('petsc@3.16.5:3.16',             when='@3.0.0-alpha6')
    depends_on('petsc@3.14.0:3.14,3.15.1:3.16', when='@3.0.0-alpha5')
    depends_on('petsc@3.14.0:3.14,3.15.1:3.15', when='@3.0.0-alpha4')
    depends_on('pkgconfig', type='build')
    depends_on('cmake@3.10:', type='build')
    depends_on('petsc+mpi+hdf5')
    depends_on('hdf5@1.10:+mpi+fortran')

    patch('CMakeDebugRelease.patch', when='@3.0.0-alpha4')

    variant('build_type', default='DebugRelease',
            description='The build type to build',
            values=('Debug', 'Release', 'DebugRelease'))

    def cmake_args(self):
        return [self.define('DAMASK_SOLVER', 'mesh')]

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def execute(self):
        with working_dir(self.build_directory):
            damask_mesh = Executable('src/DAMASK_mesh')
            damask_mesh('--help')
