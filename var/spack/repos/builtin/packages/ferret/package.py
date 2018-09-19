##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class Ferret(Package):
    """Ferret is an interactive computer visualization and analysis environment
       designed to meet the needs of oceanographers and meteorologists
       analyzing large and complex gridded data sets."""
    homepage = "http://ferret.pmel.noaa.gov/Ferret/home"
    url      = "ftp://ftp.pmel.noaa.gov/ferret/pub/source/fer_source.v696.tar.gz"

    version('6.96', '51722027c864369f41bab5751dfff8cc')

    depends_on("hdf5~mpi~fortran")
    depends_on("netcdf~mpi")
    depends_on("netcdf-fortran")
    depends_on("readline")
    depends_on("zlib")

    def url_for_version(self, version):
        return "ftp://ftp.pmel.noaa.gov/ferret/pub/source/fer_source.v{0}.tar.gz".format(
            version.joined)

    def patch(self):
        hdf5_prefix = self.spec['hdf5'].prefix
        netcdff_prefix = self.spec['netcdf-fortran'].prefix
        readline_prefix = self.spec['readline'].prefix
        libz_prefix = self.spec['zlib'].prefix

        filter_file(r'^BUILDTYPE.+',
                    'BUILDTYPE = x86_64-linux',
                    'FERRET/site_specific.mk')
        filter_file(r'^INSTALL_FER_DIR.+',
                    'INSTALL_FER_DIR = %s' % self.spec.prefix,
                    'FERRET/site_specific.mk')
        filter_file(r'^HDF5_DIR.+',
                    'HDF5_DIR = %s' % hdf5_prefix,
                    'FERRET/site_specific.mk')
        filter_file(r'^NETCDF4_DIR.+',
                    'NETCDF4_DIR = %s' % netcdff_prefix,
                    'FERRET/site_specific.mk')
        filter_file(r'^READLINE_DIR.+',
                    'READLINE_DIR = %s' % readline_prefix,
                    'FERRET/site_specific.mk')
        filter_file(r'^LIBZ_DIR.+',
                    'LIBZ_DIR = %s' % libz_prefix,
                    'FERRET/site_specific.mk')
        filter_file(r'^JAVA_HOME.+',
                    ' ',
                    'FERRET/site_specific.mk')
        filter_file(r'-lm',
                    '-lgfortran -lm',
                    'FERRET/platform_specific.mk.x86_64-linux')

    def install(self, spec, prefix):
        hdf5_prefix = spec['hdf5'].prefix
        netcdff_prefix = spec['netcdf-fortran'].prefix
        netcdf_prefix = spec['netcdf'].prefix
        libz_prefix = spec['zlib'].prefix
        ln = which('ln')
        ln('-sf',
           hdf5_prefix + '/lib',
           hdf5_prefix + '/lib64')
        ln('-sf',
           netcdff_prefix + '/lib',
           netcdff_prefix + '/lib64')
        ln('-sf',
           netcdf_prefix + '/lib/libnetcdf.a',
           netcdff_prefix + '/lib/libnetcdf.a')
        ln('-sf',
           netcdf_prefix + '/lib/libnetcdf.la',
           netcdff_prefix + '/lib/libnetcdf.la')
        ln('-sf',
           libz_prefix + '/lib',
           libz_prefix + '/lib64')

        if 'LDFLAGS' in env and env['LDFLAGS']:
            env['LDFLAGS'] += ' ' + '-lquadmath'
        else:
            env['LDFLAGS'] = '-lquadmath'

        with working_dir('FERRET', create=False):
            os.environ['LD_X11'] = '-L/usr/lib/X11 -lX11'
            os.environ['HOSTTYPE'] = 'x86_64-linux'
            make(parallel=False)
            make("install")
