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

class Mysql(Package):
    """The MySQL software delivers a very fast, multi-threaded, multi-user,
       and robust SQL (Structured Query Language) database server."""

    homepage = "http://dev.mysql.com/"
    url      = """http://pkgs.fedoraproject.org/repo/pkgs/community-mysql/
                  mysql-5.7.11.tar.gz/f84d945a40ed876d10f8d5a7f4ccba32/
                  mysql-5.7.11.tar.gz"""
    list_url = "http://pkgs.fedoraproject.org/repo/pkgs/community-mysql/"

    version('5.7.11', 'f84d945a40ed876d10f8d5a7f4ccba32',
         url=list_url+"mysql-5.7.11.tar.gz/f84d945a40ed876d10f8d5a7f4ccba32"\
              "/mysql-5.7.11.tar.gz")
    version('5.5.30', 'de881c1940aa05e78266e77c9ac3d129',
         url=list_url+"mysql-5.5.30.tar.gz/de881c1940aa05e78266e77c9ac3d129"\
              "/mysql-5.5.30.tar.gz")
    version('5.5.27', '070340bc98dcb7f646287c97f1b91a1e',
         url=list_url+"mysql-5.5.27.tar.gz/070340bc98dcb7f646287c97f1b91a1e"\
              "/mysql-5.5.27.tar.gz")
    version('5.5.19', 'a78cf450974e9202bd43674860349b5a',
        url=list_url+"mysql-5.5.19.tar.gz/a78cf450974e9202bd43674860349b5a"\
              "/mysql-5.5.19.tar.gz")
    version('5.5.18', '38b65815249f3bcacf3b0ee85171c486',
        url=list_url+"mysql-5.5.18.tar.gz/38b65815249f3bcacf3b0ee85171c486"\
              "/mysql-5.5.18.tar.gz")

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
            '-DCMAKE_PREFIX_PATH=%s' % join_path(spec['openssl'].prefix),
            '-DWITH_SSL=%s' % join_path(spec['openssl'].prefix),
            '-DDOWNLOAD_BOOST=1',
            '-DWITH_BOOST='+build_directory+'/boost',
            '-DCMAKE_C_FLAGS=-static-libgcc -lcrypto -lz -ldl',
        ])

        cmake_args.extend(std_cmake_args)

        with working_dir(build_directory, create=True):
            cmake(source_directory,*cmake_args)
            make()
            make("install")
