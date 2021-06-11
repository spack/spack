# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#Date 10-June-2021

from spack import *

class PyAnuga(PythonPackage):
    """ANUGA (pronounced "AHnooGAH") is open-source software for the simulation
    of the shallow water equation, in particular it can be used to model
    tsunamis and floods."""

    homepage = "https://github.com/GeoscienceAustralia/anuga_core"
    url      = "https://github.com/GeoscienceAustralia/anuga_core/archive/2.1.tar.gz"
    git      = "https://github.com/GeoscienceAustralia/anuga_core.git"

    maintainers = ['samcom12', 'adamjstewart']
    version('master',  branch='master')
    version('anuga_py3',  branch='anuga_py3')
    version('anuga_py2', branch='anuga_py2')
    version('2.1', sha256='0e56c4a7d55570d7b2c36fa9b53ee4e7b85f62be0b4c03ad8ab5f51464321d2f')

    variant('mpi', default=True, description='Install anuga_parallel')
    variant('openmp', default=True, description='Install with OpenMP support')
    # At present AnuGA has only been run and tested using python 2.x.
    # We recommend python 2.7.
    depends_on('python@2.6:2.8', type=('build', 'link', 'run'), when='@anuga_py2')
    depends_on('python@3.6:3.9', type=('build', 'link', 'run'), when='@anuga_py3')
    depends_on('py-setuptools@:44', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('gdal', type=('build', 'run'))
    depends_on('py-pygdal', type=('build', 'run'))
    depends_on('py-netcdf4', type=('build', 'run'))
    depends_on('py-nose', type=('build', 'run'))
    depends_on('py-dill', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))
    depends_on('py-future', type=('build', 'run'))
    depends_on('py-intel-openmp', type=('build', 'run'))
    depends_on('py-mpi4py', type=('build', 'run'),  when='@anuga_py3')
    depends_on('py-gitpython', type=('build', 'run'))
    depends_on('py-pip', type=('build'))
    depends_on('triangle', type=('build', 'run'))
    depends_on('py-pmw', type=('build', 'run'))
    depends_on('py-pyproj', type=('build', 'run'))
    depends_on('py-pymetis', type=('build', 'run'))
    depends_on('py-pypar', type=('build', 'run'), when='anuga_py2')
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-triangle', type=('build', 'run'))

    def setup_build_environment(self, env):
        if self.spec['mpi'].name == 'mpich':
            env.set('ANUGA_PARALLEL', 'mpich2')
        elif self.spec['mpi'].name == 'openmpi':
            env.set('ANUGA_PARALLEL', 'openmpi')
        elif self.spec['mpi'].name == 'intel-mpi':
            env.set('ANUGA_PARALLEL', 'intelmpi')
