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


class Cdo(Package):
    """CDO is a collection of command line Operators to manipulate and analyse
    Climate and NWP model Data. """

    homepage = "https://code.zmaw.de/projects/cdo"

    version('1.7.2', 'f08e4ce8739a4f2b63fc81a24db3ee31', url='https://code.zmaw.de/attachments/download/12760/cdo-1.7.2.tar.gz')
    version('1.6.9', 'bf0997bf20e812f35e10188a930e24e2', url='https://code.zmaw.de/attachments/download/10198/cdo-1.6.9.tar.gz')

    variant('szip', default=True, description='Enable szip compression for GRIB1')
    variant('hdf5', default=False, description='Enable HDF5 support')
    variant('netcdf', default=True, description='Enable NetCDF support')
    variant('udunits2', default=True, description='Enable UDUNITS2 support')
    variant('grib', default=True, description='Enable GRIB_API support')
    variant('libxml2', default=True, description='Enable libxml2 support')
    variant('proj', default=True, description='Enable PROJ library for cartographic projections')
    variant('curl', default=True, description='Enable curl support')
    variant('fftw', default=True, description='Enable support for fftw3')
    variant('magics', default=True, description='Enable Magics library support')

    depends_on('szip', when='+szip')
    depends_on('netcdf', when='+netcdf')
    depends_on('hdf5+threadsafe', when='+hdf5')
    depends_on('udunits2', when='+udunits2')
    depends_on('grib-api', when='+grib')
    depends_on('libxml2', when='+libxml2')
    depends_on('proj', when='+proj')
    depends_on('curl', when='+curl')
    depends_on('fftw', when='+fftw')
    depends_on('magics', when='+magics') 

    def install(self, spec, prefix):
        config_args = ["--prefix=" + prefix,
                       "--enable-shared",
                       "--enable-static"]

        if '+szip' in spec:
            config_args.append('--with-szlib=' + spec['szip'].prefix)
        else:
            config_args.append('--without-szlib')

        if '+hdf5' in spec:
            config_args.append('--with-hdf5=' + spec['hdf5'].prefix)
        else:
            config_args.append('--without-hdf5')

        if '+netcdf' in spec:
            config_args.append('--with-netcdf=' + spec['netcdf'].prefix)
        else:
            config_args.append('--without-netcdf')

        if '+udunits2' in spec:
            config_args.append('--with-udunits2=' + spec['udunits2'].prefix)
        else:
            config_args.append('--without-udunits2')

        if '+grib' in spec:
            config_args.append('--with-grib_api=' + spec['grib-api'].prefix)
        else:
            config_args.append('--without-grib_api')

        if '+libxml2' in spec:
            config_args.append('--with-libxml2=' + spec['libxml2'].prefix)
        else:
            config_args.append('--without-libxml2')

        if '+proj' in spec:
            config_args.append('--with-proj=' + spec['proj'].prefix)
        else:
            config_args.append('--without-proj')

        if '+curl' in spec:
            config_args.append('--with-curl=' + spec['curl'].prefix)
        else:
            config_args.append('--without-curl')

        if '+fftw' in spec:
            config_args.append('--with-fftw3')
        else:
            config_args.append('--without-fftw3')

        if '+magics' in spec:
            config_args.append('--with-magics=' + spec['magics'].prefix)
        else:
            config_args.append('--without-magics')

        configure(*config_args)

        make()
        make('install')
