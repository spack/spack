# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class H5hut(AutotoolsPackage):
    """H5hut (HDF5 Utility Toolkit).
    High-Performance I/O Library for Particle-based Simulations."""

    homepage = "https://amas.psi.ch/H5hut/"
    url      = "https://amas.psi.ch/H5hut/raw-attachment/wiki/DownloadSources/H5hut-1.99.13.tar.gz"

    version('1.99.13', '2a07a449afe50534de006ac6954a421a')

    variant('fortran', default=True, description='Enable Fortran support')
    variant('mpi',     default=True, description='Enable MPI support')

    depends_on('mpi',                 when='+mpi')
    # h5hut +mpi uses the obsolete function H5Pset_fapl_mpiposix:
    depends_on('hdf5@1.8:1.8.12+mpi', when='+mpi')
    depends_on('hdf5@1.8:',           when='~mpi')

    # If built in parallel, the following error message occurs:
    # install: .libs/libH5hut.a: No such file or directory
    parallel = False

    @run_before('configure')
    def validate(self):
        """Checks if Fortran compiler is available."""

        if '+fortran' in self.spec and not self.compiler.fc:
            raise RuntimeError(
                'Cannot build Fortran variant without a Fortran compiler.')

    def configure_args(self):
        spec = self.spec
        config_args = ['--enable-shared']

        if '+fortran' in spec:
            config_args.append('--enable-fortran')

        if '+mpi' in spec:
            config_args.extend([
                '--enable-parallel',
                'CC={0}'.format(spec['mpi'].mpicc),
                'CXX={0}'.format(spec['mpi'].mpicxx)
            ])

            if '+fortran' in spec:
                config_args.append('FC={0}'.format(spec['mpi'].mpifc))

        return config_args
