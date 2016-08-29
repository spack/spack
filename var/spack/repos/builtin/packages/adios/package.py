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
import os


class Adios(Package):
    """
    The Adaptable IO System (ADIOS) provides a simple,
    flexible way for scientists to describe the
    data in their code that may need to be written,
    read, or processed outside of the running simulation
    """

    homepage = "http://www.olcf.ornl.gov/center-projects/adios/"
    url      = "https://github.com/ornladios/ADIOS/archive/v1.10.0.tar.gz"

    version('1.10.0', 'eff450a4c0130479417cfd63186957f3')
    version('1.9.0' , '310ff02388bbaa2b1c1710ee970b5678')
    version('1.8.0' , 'c9116ec31e6b386f0e6ea5ab675c57e9')
    version('1.7.0' , '266897ee3a390985d840bbe2935b4293')
    version('1.6.0' , 'b3c735f3afbf552ec0d5e8152bffd778')

    variant('shared', default=True,
            description='Builds a shared version of the library')

    variant('fortran', default=True,
            description='Enable Fortran bindings support')

    variant('mpi', default=False, description='Enable MPI support')
    variant('infiniband', default=False, description='Enable infiniband support')

    variant('zlib', default=True, description='Enable szip transform support')
    variant('szip', default=False, description='Enable szip transform support')
    variant('hdf5', default=False, description='Enable HDF5 transport support')
    variant('netcdf', default=False, description='Enable NetCDF transport support')

    # Lots of setting up here for this package
    # module swap PrgEnv-intel PrgEnv-$COMP
    # module load cray-netcdf/4.3.3.1
    # module load cray-hdf5/1.8.14
    # module load python/2.7.10

    depends_on('autoconf')
    depends_on('automake')
    depends_on('libtool')
    depends_on('python')

    depends_on('mpi', when='+mpi')
    # shipped within ADIOS 1.10.0+
    depends_on('mxml', when='@:1.9.0')
    # optional transformations
    depends_on('zlib', when='+zlib')
    depends_on('szip', when='+szip')
    # optional transports
    depends_on('hdf5', when='+hdf5')
    depends_on('netcdf', when='+netcdf')

    def validate(self, spec):
        """
        Checks if incompatible variants have been activated at the same time
        :param spec: spec of the package
        :raises RuntimeError: in case of inconsistencies
        """
        if '+fortran' in spec and not self.compiler.fc:
            msg = 'cannot build a fortran variant without a fortran compiler'
            raise RuntimeError(msg)

    def install(self, spec, prefix):
        self.validate(spec)
        # Handle compilation after spec validation
        extra_args = []

        # required, otherwise building its python bindings on ADIOS will fail
        extra_args.append("CFLAGS=-fPIC")

        # MXML is shipped within ADIOS in 1.10.0+
        if spec.satisfies('@:1.9.0'):
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
        if '+hdf5' in spec:
            extra_args.append('--with-hdf5=%s' % spec['hdf5'].prefix)
        if '+netcdf' in spec:
            extra_args.append('--with-netcdf=%s' % os.environ["NETCDF_DIR"])

        if spec.satisfies('%gcc'):
            extra_args.extend(["CC=gcc", "CXX=g++"])
            if '+fortran' in spec:
                extra_args.extend(["FC=gfortran"])

        sh = which('sh')
        sh('./autogen.sh')

        configure("--prefix=%s" % prefix,
                  *extra_args)
        make()
        make("install")
