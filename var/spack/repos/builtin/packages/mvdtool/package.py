# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Mvdtool(CMakePackage):
    """MVD3 neuroscience file format parser and tool"""

    homepage = "https://github.com/BlueBrain/MVDTool"
    url      = "https://github.com/BlueBrain/MVDTool.git"
    git      = "https://github.com/BlueBrain/MVDTool.git"

    version('develop', git=url)
    version('2.1.0', tag='v2.1.0', clean=False)
    version('2.0.0', tag='v2.0.0', clean=False)
    version('1.5.1', tag='v1.5.1')
    version('1.5', tag='v1.5')
    version('1.4', tag='v1.4')

    variant('mpi', default=True, description="Enable MPI backend")
    variant('python', default=False, description="Enable Python bindings")

    depends_on('boost')
    depends_on('cmake', type='build')

    depends_on('hdf5+mpi', when='+mpi')
    depends_on('hdf5~mpi', when='~mpi')
    depends_on('highfive+mpi', when='+mpi')
    depends_on('highfive~mpi', when='~mpi')
    depends_on('mpi', when='+mpi')

    depends_on('libsonata+mpi', when='@2.1: +mpi')
    depends_on('libsonata~mpi', when='@2.1: ~mpi')

    depends_on('python', when='+python')
    depends_on('py-cython', when='+python')
    depends_on('py-numpy', when='+python')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('+mpi'):
            args.extend([
                '-DCMAKE_C_COMPILER:STRING={}'.format(self.spec['mpi'].mpicc),
                '-DCMAKE_CXX_COMPILER:STRING={}'.format(self.spec['mpi'].mpicxx),
            ])
        if self.spec.satisfies('+python'):
            args.extend([
                '-DBUILD_PYTHON_BINDINGS:BOOL=ON'
            ])
        return args

    @when('+python')
    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        site_dir = self.spec['python'].package.site_packages_dir.split(os.sep)[1:]
        for target in (self.prefix.lib, self.prefix.lib64):
            pathname = os.path.join(target, *site_dir)
            if os.path.isdir(pathname):
                run_env.prepend_path('PYTHONPATH', pathname)
