# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shutil

from spack import *


class PyAnuga(PythonPackage):
    """ANUGA (pronounced "AHnooGAH") is open-source software for the simulation
    of the shallow water equation, in particular it can be used to model
    tsunamis and floods."""

    homepage = "https://github.com/GeoscienceAustralia/anuga_core"
    url      = "https://github.com/GeoscienceAustralia/anuga_core/archive/2.1.tar.gz"
    git      = 'https://github.com/GeoscienceAustralia/anuga_core.git'

    # The git main branch of the repo is now python3-only
    version('master', branch='main')
    version('2.1', sha256='0e56c4a7d55570d7b2c36fa9b53ee4e7b85f62be0b4c03ad8ab5f51464321d2f')

    variant('mpi', default=True, description='Install anuga_parallel')

    # Non-versioned dependencies for Anuga main and future versions based on python@3.5:
    depends_on('python@3.5:',            type=('build', 'run'), when='@2.2:')
    depends_on('gdal+geos+python',       type=('build', 'run'), when='@2.2:')
    depends_on('py-future',              type=('build', 'run'), when='@2.2:')
    depends_on('py-matplotlib',          type=('build', 'run'), when='@2.2:')
    depends_on('py-numpy',               type=('build', 'run'), when='@2.2:')
    depends_on('py-setuptools',          type=('build'),        when='@2.2:')
    # Replaces pyar in python3 anuga:
    depends_on('py-mpi4py',              type=('build', 'run'), when='@2.2:+mpi')
    depends_on('py-dill',                type=('test'))
    depends_on('py-nose',                type=('test'))
    depends_on('py-scipy',               type=('test'))
    depends_on('py-triangle',            type=('test'))

    # Version-restricted dependencies for anuga@:2.1, converted to use when='@:2.1':
    depends_on('python@2.6:2.7.18',      type=('build', 'run'), when='@:2.1')
    depends_on('gdal@:3.2+geos+python',  type=('build', 'run'), when='@:2.1')
    depends_on('py-matplotlib@:2',       type=('build', 'run'), when='@:2.1')
    depends_on('py-numpy@:1.16',         type=('build', 'run'), when='@:2.1')
    depends_on('py-setuptools@:44',      type=('build'),        when='@:2.1')
    # Workaround for problem in the original concretizer selecting 3.6, wanting python3:
    depends_on('py-setuptools-scm@:3.5', type=('build'),        when='@:2.1')
    # pypar is not updated for python3, for python3, py-mpi4py is unsed instead:
    depends_on('py-pypar',               type=('build', 'run'), when='@:2.1+mpi')

    # Unversioned dependencies of the python2 and python3-based versions
    depends_on('py-cython',              type=('build'))
    depends_on('py-netcdf4', type=('build', 'run'))

    # https://github.com/GeoscienceAustralia/anuga_core/issues/247
    conflicts('%apple-clang@12:')

    def patch(self):
        # MPI tests can only be activated when=+mpi and mpiexec is added to the PATH
        shutil.rmtree('anuga/parallel/tests')
        # AttributeError: 'NoneType' object has no attribute 'Intersection'
        shutil.rmtree('anuga/utilities/tests')
        # These use csv files from anuga/utilities/tests/data
        shutil.rmtree('anuga/geometry/tests')

    install_time_test_callbacks = ['test', 'installtest']

    def installtest(self):
        python('runtests.py', '--no-build')
