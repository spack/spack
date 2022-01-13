# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMvdtool(PythonPackage):
    """Python bindings for the MVD3 neuroscience file format parser and tool
    """

    homepage = "https://github.com/BlueBrain/MVDTool"
    url      = "https://github.com/BlueBrain/MVDTool.git"
    git      = "https://github.com/BlueBrain/MVDTool.git"

    version('develop', branch='master', submodules=True, get_full_repo=False)
    version('2.4.2', tag='v2.4.2', submodules=True, get_full_repo=False)
    version('2.4.0', tag='v2.4.0', submodules=True, get_full_repo=False)
    version('2.3.6', tag='v2.3.6', submodules=True, get_full_repo=False)
    version('2.3.5', tag='v2.3.5', submodules=True, get_full_repo=False)
    version('2.3.4', tag='v2.3.4', submodules=True, get_full_repo=False)
    version('2.3.3', tag='v2.3.3', submodules=True, get_full_repo=False)
    version('2.3.2', tag='v2.3.2', submodules=True, get_full_repo=False)
    version('2.3.1', tag='v2.3.1', submodules=True, get_full_repo=False)
    version('2.3.0', tag='v2.3.0', submodules=True, get_full_repo=False)
    version('2.2.1', tag='v2.2.1', submodules=True, get_full_repo=False)

    variant('mpi', default=True, description='Build with support for MPI')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    depends_on('cmake@3.2:', type='build')
    depends_on('py-numpy', type='run')

    depends_on('boost')
    depends_on('mpi', when='+mpi')
    depends_on('hdf5+mpi', type=('build', 'run'), when="+mpi")
    depends_on('hdf5~mpi', type=('build', 'run'), when="~mpi")
    depends_on('libsonata~mpi', type=('build', 'run'), when='~mpi@2.1:')
    depends_on('libsonata+mpi', type=('build', 'run'), when='+mpi@2.1:')
    depends_on('highfive~mpi', type='build', when='~mpi')
    depends_on('highfive+mpi', type='build', when='+mpi')

    @run_before('build')
    def configure(self):
        # we cant use @when('+mpi'), raises NoSuchMethodError
        if self.spec.satisfies('+mpi'):
            env['CC'] = self.spec['mpi'].mpicc
            env['CXX'] = self.spec['mpi'].mpicxx
