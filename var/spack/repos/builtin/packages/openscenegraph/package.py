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
################################################################################
# Copyright (c) 2015-2016 Krell Institute. All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
################################################################################

from spack import *


class Openscenegraph(Package):
    """TODO(JRC)"""

    homepage = "http://www.openscenegraph.org"
    url      = "http://trac.openscenegraph.org/downloads/developer_releases/OpenSceneGraph-3.4.0.zip"

    version('3.4.0', 'a5e762c64373a46932e444f6f7332496')
    version('3.2.3', '02ffdad7744c747d8fad0d7babb58427')

    variant('debug', default=False, description='Builds a debug version of the library')
    variant('shared', default=True, description='Builds a shared version of the library')

    depends_on('cmake@2.8.7:', type='build')
    depends_on('qt@4:')
    depends_on('zlib')

    def install(self, spec, prefix):
        cmake_args = std_cmake_args[:]
        cmake_args.extend([
            '-DCMAKE_BUILD_TYPE=%s' % ('Release' if '+debug' in spec else 'Debug'),
            '-DDYNAMIC_OPENSCENEGRAPH=%s' % ('ON' if '+shared' in spec else 'OFF'),
            '-DDYNAMIC_OPENTHREADS=%s' % ('ON' if '+shared' in spec else 'OFF'),
        ])

        source_directory = self.stage.source_path
        build_directory = join_path(source_directory, 'spack-build')
        with working_dir(build_directory, create=True):
            cmake(
                source_directory,
                '-DCMAKE_INSTALL_PREFIX=%s' % prefix,
                '-DCMAKE_C_COMPILER=%s' % self.compilers.cc,
                '-DCMAKE_CXX_COMPILER=%s' % self.compilers.cxx,
                '-DZLIB_INCLUDE_DIR=%s' % spec['zlib'].prefix.include,
                '-DZLIB_LIBRARY=%s/libz.so' % spec['zlib'].prefix.lib,
                '-DBUILD_OSG_APPLICATIONS=OFF',
                '-DFFMPEG_LIBAVCODEC_INCLUDE_DIRS=""',
                '-DFFMPEG_LIBAVFORMAT_INCLUDE_DIRS=""',
                '-DFFMPEG_LIBAVUTIL_INCLUDE_DIRS=""',
                '-DOSG_NOTIFY_DISABLED=ON',
                '-DLIB_POSTFIX=""',
                *cmake_args
            )
            make()
            make('install')
