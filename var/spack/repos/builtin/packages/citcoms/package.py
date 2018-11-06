# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Citcoms(AutotoolsPackage):
    """CitcomS is a finite element code designed to solve compressible
    thermochemical convection problems relevant to Earth's mantle."""

    homepage = "https://geodynamics.org/cig/software/citcoms/"
    url      = "https://github.com/geodynamics/citcoms/archive/v3.2.0.tar.gz"

    version('3.2.0', sha256='7334efe7e464b3be328aa49c95110112e945f2b934d1a69da98851993e4ed421')

    variant('pyre', default=False, description='build Pyre modules')
    variant('exchanger', default=False, description='use Exchanger')
    variant('ggrd', default=False, description='use GGRD file support')
    variant('cuda', default=False, description='use CUDA')
    variant('hdf5', default=False, description='add HDF5 support')

    # Build dependencies
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')

    # Required dependencies
    depends_on('mpi')

    # Optional dependencies
    # Please note that Pyre in CitcomS does not work with Python 2.7 or higher.
    depends_on('python', type=('build', 'run', 'link'), when='+pyre')
    depends_on('py-pythia', type=('build', 'run'), when='+pyre')
    depends_on('hdf5+mpi', when='+hdf5')

    def configure_args(self):
        args = []

        if '+pyre' in self.spec:
            args.append('--with-pyre')
        else:
            args.append('--without-pyre')

        if '+exchanger' in self.spec:
            args.append('--with-exchanger')
        else:
            args.append('--without-exchanger')

        if '+ggrd' in self.spec:
            args.append('--with-ggrd')
        else:
            args.append('--without-ggrd')

        if '+cuda' in self.spec:
            args.append('--with-cuda')
        else:
            args.append('--without-cuda')

        if '+hdf5' in self.spec:
            args.append('--with-hdf5')
        else:
            args.append('--without-hdf5')

        return args
