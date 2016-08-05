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


class Openscenegraph(Package):
    """TODO(JRC)"""

    homepage = "http://www.openscenegraph.org"
    url      = "http://trac.openscenegraph.org/downloads/developer_releases/OpenSceneGraph-3.2.3.zip"

    version('3.2.3', '02ffdad7744c747d8fad0d7babb58427')
    version('3.1.5', '1c90b851b109849c985006486ef59822')

    variant('debug', default=False, description='Builds a debug version of the library')
    variant('shared', default=True, description='Builds a shared version of the library')

    depends_on('cmake@2.8.7:', type='build')
    depends_on('qt@4:')
    depends_on('zlib')

    def install(self, spec, prefix):
        build_type = 'Debug' if '+debug' in spec else 'Release'
        shared_status = 'ON' if '+shared' in spec else 'OFF'

        cmake_args = std_cmake_args[:]
        cmake_args.extend([
            '-DCMAKE_BUILD_TYPE={0}'.format(build_type),
            '-DDYNAMIC_OPENSCENEGRAPH={0}'.format(shared_status),
            '-DDYNAMIC_OPENTHREADS={0}'.format(shared_status),
        ])

        source_directory = self.stage.source_path
        build_directory = join_path(source_directory, 'spack-build')
        with working_dir(build_directory, create=True):
            cmake(
                source_directory,
                '-DCMAKE_INSTALL_PREFIX={0}'.format(prefix),
                '-DCMAKE_C_COMPILER={0}'.format(self.compiler.cc),
                '-DCMAKE_CXX_COMPILER={0}'.format(self.compiler.cxx),
                '-DZLIB_INCLUDE_DIR={0}'.format(spec['zlib'].prefix.include),
                '-DZLIB_LIBRARY={0}/libz.so'.format(spec['zlib'].prefix.lib),
                '-DBUILD_OSG_APPLICATIONS=OFF',
                '-DOSG_NOTIFY_DISABLED=ON',
                '-DLIB_POSTFIX=',
                '-DFFMPEG_LIBAVCODEC_INCLUDE_DIRS=',
                '-DFFMPEG_LIBAVFORMAT_INCLUDE_DIRS=',
                '-DFFMPEG_LIBAVUTIL_INCLUDE_DIRS=',
                *cmake_args
            )
            make()
            make('install')
