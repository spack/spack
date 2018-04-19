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


class Mysql(Package):
    """The MySQL software delivers a very fast, multi-threaded, multi-user,
    and robust SQL (Structured Query Language) database server."""

    homepage = "http://dev.mysql.com/"
    url      = "http://pkgs.fedoraproject.org/repo/pkgs/community-mysql/mysql-5.7.11.tar.gz/f84d945a40ed876d10f8d5a7f4ccba32/mysql-5.7.11.tar.gz"
    list_url = "http://pkgs.fedoraproject.org/repo/pkgs/community-mysql/"

    version('5.7.11', 'f84d945a40ed876d10f8d5a7f4ccba32',
         url="http://pkgs.fedoraproject.org/repo/pkgs/community-mysql/mysql-5.7.11.tar.gz/f84d945a40ed876d10f8d5a7f4ccba32/mysql-5.7.11.tar.gz")
    version('5.5.30', '382ab22fd33ec4fb65ecd61d92b61736',
         url="http://pkgs.fedoraproject.org/repo/pkgs/community-mysql/mysql-5.5.30-nodocs.tar.gz/382ab22fd33ec4fb65ecd61d92b61736/mysql-5.5.30-nodocs.tar.gz")
    version('5.5.27', 'fc115ac6b28412298886651cffc70ccf',
         url="http://pkgs.fedoraproject.org/repo/pkgs/mysql/mysql-5.5.27-nodocs.tar.gz/fc115ac6b28412298886651cffc70ccf/mysql-5.5.27-nodocs.tar.gz")
    version('5.5.19', '76c434e3db654f59d06b220daaeeed39',
        url="http://pkgs.fedoraproject.org/repo/pkgs/mysql/mysql-5.5.19-nodocs.tar.gz/76c434e3db654f59d06b220daaeeed39/mysql-5.5.19-nodocs.tar.gz")
    version('5.5.18', '22e4bbacb27efdb38c0b54b5c5fab3e8',
        url="http://pkgs.fedoraproject.org/repo/pkgs/mysql/mysql-5.5.18-nodocs.tar.gz/22e4bbacb27efdb38c0b54b5c5fab3e8/mysql-5.5.18-nodocs.tar.gz")

    patch('mysql-5.7.11.patch', when='@5.7.11')

    depends_on('cmake', type='build')
    depends_on('openssl')
    depends_on('libaio')

    def install(self, spec, prefix):
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path

        cmake_args = []

        if '+debug' in spec:
            cmake_args.append('-DCMAKE_BUILD_TYPE:STRING=Debug')
        else:
            cmake_args.append('-DCMAKE_BUILD_TYPE:STRING=Release')

        cmake_args.extend([
            '-DDOWNLOAD_BOOST=1',
            '-DWITH_BOOST=' + build_directory + '/boost',
            '-DCMAKE_C_FLAGS=-static-libgcc -lcrypto -lz -ldl',
        ])

        if spec.satisfies('@:5.5'):
            cmake_args.append('-DWITH_SSL=yes')
        else:
            sslprefix = spec['openssl'].prefix
            cmake_args.append('-DWITH_SSL=%s' % join_path(sslprefix))
            cmake_args.append('-DCMAKE_PREFIX_PATH=%s' % join_path(sslprefix))

        cmake_args.extend(std_cmake_args)

        cmake_args.extend(std_cmake_args)

        with working_dir(build_directory, create=True):
            cmake(source_directory, *cmake_args)
            make()
            make("install")
