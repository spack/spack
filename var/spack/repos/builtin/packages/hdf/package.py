# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    version('4.2.13', 'a6aa950b3fce5162b96496d8ea0b82bf')
    version('4.2.12', '79fd1454c899c05e34a3da0456ab0c1c')
    version('4.2.11', '063f9928f3a19cc21367b71c3b8bbf19')

    variant('szip', default=False, description="Enable szip support")

    depends_on('jpeg@6b:')
    depends_on('szip', when='+szip')
    depends_on('zlib@1.1.4:')

    depends_on('bison', type='build')
    depends_on('flex',  type='build')

    def configure_args(self):
        spec = self.spec

        config_args = [
            'CFLAGS={0}'.format(self.compiler.pic_flag),
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

        return config_args
