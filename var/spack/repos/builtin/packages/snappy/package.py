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


class Snappy(CMakePackage):
    """A fast compressor/decompressor: https://code.google.com/p/snappy"""

    homepage = "https://github.com/google/snappy"
    url      = "https://github.com/google/snappy/archive/1.1.7.tar.gz"

    version('1.1.7', 'ee9086291c9ae8deb4dac5e0b85bf54a')

    variant('shared', default=True, description='Build shared libraries')
    variant('pic', default=True, description='Build position independent code')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DCMAKE_INSTALL_LIBDIR:PATH={0}'.format(
                self.prefix.lib),
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF')
        ]

        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if '+pic' in self.spec and name in ('cflags', 'cxxflags'):
            flags.append(self.compiler.pic_flag)
        return (None, None, flags)

    @run_after('install')
    def install_pkgconfig(self):
        mkdirp(self.prefix.lib.pkgconfig)

        with open(join_path(self.prefix.lib.pkgconfig, 'snappy.pc'), 'w') as f:
            f.write('prefix={0}\n'.format(self.prefix))
            f.write('exec_prefix=${prefix}\n')
            f.write('libdir={0}\n'.format(self.prefix.lib))
            f.write('includedir={0}\n'.format(self.prefix.include))
            f.write('\n')
            f.write('Name: Snappy\n')
            f.write('Description: A fast compressor/decompressor.\n')
            f.write('Version: {0}\n'.format(self.spec.version))
            f.write('Cflags: -I${includedir}\n')
            f.write('Libs: -L${libdir} -lsnappy\n')
