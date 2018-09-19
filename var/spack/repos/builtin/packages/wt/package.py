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


class Wt(CMakePackage):
    """Wt, C++ Web Toolkit.

    Wt is a C++ library for developing web applications."""

    homepage = "http://www.webtoolkit.eu/wt"
    url      = "https://github.com/emweb/wt/archive/3.3.7.tar.gz"
    git      = "https://github.com/emweb/wt.git"

    version('master', branch='master')
    version('3.3.7', '09858901f2dcf5c3d36a9237daba3e3f')

    # wt builds in parallel, but requires more than 5 GByte RAM per -j <njob>
    # which most machines do not provide and crash the build
    parallel = False

    variant('openssl', default=True,
            description='SSL and WebSockets support in the built-in httpd, '
                        'the HTTP(S) client, and additional cryptographic '
                        'hashes in the authentication module')
    variant('libharu', default=True, description='painting to PDF')
    # variant('graphicsmagick', default=True,
    #         description='painting to PNG, GIF')
    variant('sqlite', default=False, description='create SQLite3 DBO')
    variant('mariadb', default=False, description='create MariaDB/MySQL DBO')
    variant('postgresql', default=False, description='create PostgreSQL DBO')
    # variant('firebird', default=False, description='create Firebird DBO')
    variant('pango', default=True,
            description='improved font support in PDF and raster image '
                        'painting')
    variant('zlib', default=True,
            description='compression in the built-in httpd')
    # variant('fastcgi', default=False,
    #         description='FastCGI connector via libfcgi++')

    depends_on('boost@1.46.1:')
    depends_on('openssl', when='+openssl')
    depends_on('libharu', when='+libharu')
    depends_on('sqlite', when='+sqlite')
    depends_on('mariadb', when='+mariadb')
    depends_on('postgresql', when='+postgresql')
    depends_on('pango', when='+pango')
    depends_on('zlib', when='+zlib')

    def cmake_args(self):
        spec = self.spec

        cmake_args = [
            '-DBUILD_EXAMPLES:BOOL=OFF',
            '-DCONNECTOR_FCGI:BOOL=OFF',
            '-DENABLE_OPENGL:BOOL=OFF',
            '-DENABLE_QT4:BOOL=OFF'
        ]
        cmake_args.extend([
            '-DENABLE_SSL:BOOL={0}'.format((
                'ON' if '+openssl' in spec else 'OFF')),
            '-DENABLE_HARU:BOOL={0}'.format((
                'ON' if '+libharu' in spec else 'OFF')),
            '-DENABLE_PANGO:BOOL={0}'.format((
                'ON' if '+pango' in spec else 'OFF')),
            '-DENABLE_SQLITE:BOOL={0}'.format((
                'ON' if '+sqlite' in spec else 'OFF')),
            '-DENABLE_MYSQL:BOOL={0}'.format((
                'ON' if '+mariadb' in spec else 'OFF')),
            '-DENABLE_POSTGRES:BOOL={0}'.format((
                'ON' if '+postgres' in spec else 'OFF'))
        ])
        return cmake_args
