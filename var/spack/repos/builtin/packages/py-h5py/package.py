# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyH5py(PythonPackage):
    """The h5py package provides both a high- and low-level interface to the
    HDF5 library from Python."""

    homepage = "http://www.h5py.org/"
    url      = "https://pypi.io/packages/source/h/h5py/h5py-2.9.0.tar.gz"

    import_modules = ['h5py', 'h5py._hl']

    version('2.9.0', '9d41ca62daf36d6b6515ab8765e4c8c4388ee18e2a665701fef2b41563821002')
    version('2.8.0', 'ece4f358e69fc8a416f95953b91bc373')
    version('2.7.1', 'da630aebe3ab9fa218ac405a218e95e0')
    version('2.7.0', 'f62937f40f68d3b128b3941be239dd93')
    version('2.6.0', 'ec476211bd1de3f5ac150544189b0bf4')
    version('2.5.0', '6e4301b5ad5da0d51b0a1e5ac19e3b74')
    version('2.4.0', '80c9a94ae31f84885cc2ebe1323d6758')

    variant('mpi', default=True, description='Build with MPI support')

    # Build dependencies
    depends_on('py-cython@0.23:', type='build')
    depends_on('py-pkgconfig', type='build')
    depends_on('py-setuptools', type='build')

    # Build and runtime dependencies
    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))

    # Link dependencies
    depends_on('hdf5@1.8.4:+hl')

    # MPI dependencies
    depends_on('hdf5+mpi', when='+mpi')
    depends_on('mpi', when='+mpi')
    depends_on('py-mpi4py', when='+mpi', type=('build', 'run'))

    phases = ['configure', 'install']

    def configure(self, spec, prefix):
        self.setup_py('configure', '--hdf5={0}'.format(spec['hdf5'].prefix))

        if '+mpi' in spec:
            env['CC'] = spec['mpi'].mpicc
            self.setup_py('configure', '--mpi')
