# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hdf(AutotoolsPackage):
    """HDF4 (also known as HDF) is a library and multi-object
    file format for storing and managing data between machines."""

    homepage = "https://portal.hdfgroup.org/display/support"
    url      = "https://support.hdfgroup.org/ftp/HDF/releases/HDF4.2.14/src/hdf-4.2.14.tar.gz"
    list_url = "https://support.hdfgroup.org/ftp/HDF/releases/"
    list_depth = 2

    version('4.2.14', sha256='2d383e87c8a0ca6a5352adbd1d5546e6cc43dc21ff7d90f93efa644d85c0b14a')
    version('4.2.13', sha256='be9813c1dc3712c2df977d4960e1f13f20f447dfa8c3ce53331d610c1f470483')
    version('4.2.12', sha256='dd419c55e85d1a0e13f3ea5ed35d00710033ccb16c85df088eb7925d486e040c')
    version('4.2.11', sha256='c3f7753b2fb9b27d09eced4d2164605f111f270c9a60b37a578f7de02de86d24')

    variant('szip', default=False, description="Enable szip support")
    variant('libtirpc', default=False, description="Use xdr library from libtirpc package; if false, will use system or hdf internal")

    depends_on('jpeg@6b:')
    depends_on('szip', when='+szip')
    depends_on('libtirpc', when='+libtirpc')
    depends_on('zlib@1.1.4:')

    depends_on('bison', type='build')
    depends_on('flex',  type='build')

    def configure_args(self):
        spec = self.spec

        config_args = [
            'CFLAGS={0}'.format(self.compiler.cc_pic_flag),
            '--with-jpeg={0}'.format(spec['jpeg'].prefix),
            '--with-zlib={0}'.format(spec['zlib'].prefix),
            '--disable-netcdf',  # must be disabled to build NetCDF with HDF4
            '--enable-fortran',
            '--disable-shared',  # fortran and shared libs are not compatible
            '--enable-static',
            '--enable-production'
        ]

        # Szip support
        if '+szip' in spec:
            config_args.append('--with-szlib={0}'.format(spec['szip'].prefix))
        else:
            config_args.append('--without-szlib')

        if '+libtirpc' in spec:
            config_args.append('LIBS=-ltirpc')
            config_args.append('CPPFLAGS=-I{0}/include/tirpc'.format(
                spec['libtirpc'].prefix))

        return config_args
