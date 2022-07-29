# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class H5zZfp(MakefilePackage):
    """A highly flexible floating point and integer compression plugin for the
       HDF5 library using ZFP compression."""

    homepage = "https://h5z-zfp.readthedocs.io/en/latest"
    git      = "https://github.com/LLNL/H5Z-ZFP.git"
    url      = "https://github.com/LLNL/H5Z-ZFP/archive/refs/tags/v1.0.1.tar.gz"

    version('develop', branch='master')
    version('1.0.1', sha256='b9ed91dab8e2ef82dc6706b4242c807fb352875e3b21c217dd00782dd1a22b24')
    version('0.8.0', sha256='a5eb089191369a5e929c51ec9e5da107afaee39c6ab3b7ad693c454319ab9217')
    version('0.7.0', sha256='f728b0bcb9e9cf8bafe05909ab02fec39415635d275e98b661176f69d34f87b3')

    variant('fortran', default=True, description='Enable Fortran support')

    depends_on('hdf5+fortran', when='+fortran')
    depends_on('hdf5',         when='~fortran')
    depends_on('mpi',          when='^hdf5+mpi')
    depends_on('zfp bsws=8')

    patch('https://github.com/LLNL/H5Z-ZFP/commit/983a1870cefff5fdb643898a14eda855c2c231e4.patch?full_index=1',
          sha256='07a53b8b0d4c1df62a3f9f21b30ad0eb90f26b38eb6cacc0de6482fd8f5daea2', when='@1.0.1')
    patch('config.make.patch', when='@0.7.0:0.8.0')
    patch('config.make.0.7.0.patch', when='@0.7.0')
    patch('Makefile.0.7.0.patch', when='@0.7.0')
    patch('fj.patch', when='@0.7.0: %fj')

    @property
    def make_defs(self):
        cc = spack_cc
        fc = spack_fc
        if '^hdf5+mpi' in self.spec:
            cc = self.spec['mpi'].mpicc
            fc = self.spec['mpi'].mpifc
        make_defs = [
            'PREFIX=%s' % prefix,
            'CC=%s' % cc,
            'HDF5_HOME=%s' % self.spec['hdf5'].prefix,
            'ZFP_HOME=%s' % self.spec['zfp'].prefix]

        if '+fortran' in self.spec and fc:
            make_defs += ['FC=%s' % fc]
        else:
            make_defs += ['FC=']

        return make_defs

    @property
    def build_targets(self):
        targets = ['all']
        return self.make_defs + targets

    @property
    def install_targets(self):
        make_args = ['install']
        return make_args + self.make_defs
