##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *


class Adios(AutotoolsPackage):
    """The Adaptable IO System (ADIOS) provides a simple,
    flexible way for scientists to describe the
    data in their code that may need to be written,
    read, or processed outside of the running simulation.
    """

    homepage = "http://www.olcf.ornl.gov/center-projects/adios/"
    url      = "https://github.com/ornladios/ADIOS/archive/v1.11.1.tar.gz"

    version('develop', git='https://github.com/ornladios/ADIOS.git',
            branch='master')
    version('1.11.1', '5639bfc235e50bf17ba9dafb14ea4185')
    version('1.10.0', 'eff450a4c0130479417cfd63186957f3')
    version('1.9.0', '310ff02388bbaa2b1c1710ee970b5678')

    variant('shared', default=True,
            description='Builds a shared version of the library')

    variant('fortran', default=False,
            description='Enable Fortran bindings support')

    variant('mpi', default=True, description='Enable MPI support')
    variant('infiniband', default=False, description='Enable infiniband support')

    # transforms
    variant('zlib', default=True, description='Enable zlib transform support')
    variant('szip', default=False, description='Enable szip transform support')
    variant('zfp', default=False, description='Enable ZFP transform support')
    # transports and serial file converters
    variant('hdf5', default=False, description='Enable parallel HDF5 transport and serial bp2h5 converter')

    # Lots of setting up here for this package
    # module swap PrgEnv-intel PrgEnv-$COMP
    # module load cray-hdf5/1.8.14
    # module load python/2.7.10

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('python', type='build')

    depends_on('mpi', when='+mpi')
    depends_on('mxml@2.9:')
    # optional transformations
    depends_on('zlib', when='+zlib')
    depends_on('szip', when='+szip')
    depends_on('zfp', when='+zfp')
    # optional transports & file converters
    depends_on('hdf5@1.8:+mpi', when='+hdf5')

    build_directory = 'spack-build'

    # ADIOS uses the absolute Python path, which is too long and results in
    # "bad interpreter" errors
    patch('python.patch')
    # Fix ADIOS <=1.10.0 compile error on HDF5 1.10+
    #   https://github.com/ornladios/ADIOS/commit/3b21a8a41509
    #   https://github.com/LLNL/spack/issues/1683
    patch('adios_1100.patch', when='@:1.10.0^hdf5@1.10:')

    def validate(self, spec):
        """
        Checks if incompatible variants have been activated at the same time
        :param spec: spec of the package
        :raises RuntimeError: in case of inconsistencies
        """
        if '+fortran' in spec and not self.compiler.fc:
            msg = 'cannot build a fortran variant without a fortran compiler'
            raise RuntimeError(msg)

    def configure_args(self):
        spec = self.spec
        self.validate(spec)

        extra_args = []

        # required, otherwise building its python bindings on ADIOS will fail
        extra_args.append("CFLAGS=-fPIC")

        # always build external MXML, even in ADIOS 1.10.0+
        extra_args.append('--with-mxml=%s' % spec['mxml'].prefix)

        if '+shared' in spec:
            extra_args.append('--enable-shared')

        if '+mpi' in spec:
            extra_args.append('--with-mpi')
        if '+infiniband' in spec:
            extra_args.append('--with-infiniband')
        else:
            extra_args.append('--with-infiniband=no')

        if '+fortran' in spec:
            extra_args.append('--enable-fortran')
        else:
            extra_args.append('--disable-fortran')

        if '+zlib' in spec:
            extra_args.append('--with-zlib=%s' % spec['zlib'].prefix)
        if '+szip' in spec:
            extra_args.append('--with-szip=%s' % spec['szip'].prefix)
        if '+zfp' in spec:
            extra_args.append('--with-zfp=%s' % spec['zfp'].prefix)
        if '+hdf5' in spec:
            extra_args.append('--with-phdf5=%s' % spec['hdf5'].prefix)

        return extra_args
