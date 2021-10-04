# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class DamaskMesh(CMakePackage):
    """Mesh solver for DAMASK"""

    homepage = "https://damask3.mpie.de"
    url      = "https://damask3.mpie.de/download/damask-3.0.0.tar.xz"

    maintainers = ['MarDieh']

    version('3.0.0-alpha4', sha256='0bb8bde43b27d852b1fb6e359a7157354544557ad83d87987b03f5d629ce5493')

    depends_on('cmake@3.10:', type='build')
    depends_on('petsc@3.14.0:3.14,3.15.1:3.15')
    depends_on('hdf5+fortran')

    patch('CMakeDebugRelease.patch', when='@3.0.0-alpha4')

    variant('build_type', default='DebugRelease',
            description='The build type to build',
            values=('Debug', 'Release', 'DebugRelease'))

    def cmake_args(self):
        args = ['-DDAMASK_SOLVER:STRING=mesh']
        return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def execute(self):
        with working_dir(self.build_directory):
            damask_mesh = Executable('src/DAMASK_mesh')
            damask_mesh('--help')
