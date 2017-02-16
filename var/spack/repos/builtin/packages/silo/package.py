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


class Silo(Package):
    """Silo is a library for reading and writing a wide variety of scientific
       data to binary, disk files."""

    homepage = "http://wci.llnl.gov/simulation/computer-codes/silo"
    base_url = "https://wci.llnl.gov/content/assets/docs/simulation/computer-codes/silo"

    version('4.10.2', '9ceac777a2f2469ac8cef40f4fab49c8')
    version('4.9', 'a83eda4f06761a86726e918fc55e782a')
    version('4.8', 'b1cbc0e7ec435eb656dc4b53a23663c9')

    variant('fortran', default=True, description='Enable Fortran support')
    variant('shared', default=True, description='Build shared libraries')
    variant('silex', default=False,
            description='Builds Silex, a GUI for viewing Silo files')

    depends_on('hdf5')
    depends_on('qt', when='+silex')

    patch('remove-mpiposix.patch', when='@4.8:4.10.2')

    def install(self, spec, prefix):
        config_args = [
            '--enable-fortran' if '+fortran' in spec else '--disable-fortran',
            '--enable-silex' if '+silex' in spec else '--disable-silex',
            '--enable-shared' if '+shared' in spec else '--disable-shared',
        ]

        if '+silex' in spec:
            config_args.append('--with-Qt-dir=%s' % spec['qt'].prefix)

        configure(
            '--prefix=%s' % prefix,
            '--with-hdf5=%s,%s' % (spec['hdf5'].prefix.include,
                                   spec['hdf5'].prefix.lib),
            '--with-zlib=%s,%s' % (spec['zlib'].prefix.include,
                                   spec['zlib'].prefix.lib),
            '--enable-install-lite-headers',
            *config_args)

        make()
        make('install')

    def url_for_version(self, version):
        return '%s/silo-%s/silo-%s.tar.gz' % (Silo.base_url, version, version)
