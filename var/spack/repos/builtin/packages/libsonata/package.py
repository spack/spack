# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Libsonata(CMakePackage):
    """
    `libsonata` provides C++ / Python API for reading SONATA Nodes / Edges

    See also:
    https://github.com/AllenInstitute/sonata/blob/master/docs/SONATA_DEVELOPER_GUIDE.md
    """
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/common/libsonata"
    url      = "ssh://bbpcode.epfl.ch/common/libsonata"

    version('develop', git=url, submodules=False)

    variant('mpi', default=False, description="Enable MPI backend")
    variant('python', default=False, description="Enable Python bindings")

    depends_on('cmake@3.0:', type='build')
    depends_on('fmt@4.0:')
    depends_on('highfive+mpi', when='+mpi')
    depends_on('highfive~mpi', when='~mpi')
    depends_on('mpi', when='+mpi')

    depends_on('python', type=('build', 'run'), when='+python')
    depends_on('py-pybind11@2.0:', type='build', when='+python')

    def cmake_args(self):
        result = [
            '-DEXTLIB_FROM_SUBMODULES=OFF',
        ]
        if self.spec.satisfies('+python'):
            pyspec = self.spec['python']
            result.extend([
                '-DSONATA_PYTHON=ON',
                '-DPYTHON_INSTALL_SUFFIX={}'.format(pyspec.package.site_packages_dir),
                '-DPYTHON_EXECUTABLE:FILEPATH={}'.format(pyspec.command.path),
            ])
        if self.spec.satisfies('+mpi'):
            result.extend([
                '-DCMAKE_C_COMPILER:STRING={}'.format(self.spec['mpi'].mpicc),
                '-DCMAKE_CXX_COMPILER:STRING={}'.format(self.spec['mpi'].mpicxx),
            ])
        return result

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        if self.spec.satisfies("+python"):
            pyspec = self.spec['python']
            run_env.prepend_path(
                'PYTHONPATH',
                os.path.join(self.prefix, pyspec.package.site_packages_dir)
            )
