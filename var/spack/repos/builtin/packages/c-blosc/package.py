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

import sys

from spack import *


class CBlosc(Package):
    """Blosc, an extremely fast, multi-threaded, meta-compressor library"""
    homepage = "http://www.blosc.org"
    url      = "https://github.com/Blosc/c-blosc/archive/v1.11.1.tar.gz"

    version('1.11.1', 'e236550640afa50155f3881f2d300206')
    version('1.9.2',  'dd2d83069d74b36b8093f1c6b49defc5')
    version('1.9.1',  '7d708d3daadfacf984a87b71b1734ce2')
    version('1.9.0',  'e4c1dc8e2c468e5cfa2bf05eeee5357a')
    version('1.8.1',  'd73d5be01359cf271e9386c90dcf5b05')
    version('1.8.0',  '5b92ecb287695ba20cc33d30bf221c4f')

    variant('avx2', default=True, description='Enable AVX2 support')

    depends_on("cmake", type='build')
    depends_on("snappy")
    depends_on("zlib")

    def install(self, spec, prefix):
        avx2 = '-DDEACTIVATE_AVX2=%s' % ('ON' if '~avx2' in spec else 'OFF')
        cmake('.', avx2, *std_cmake_args)

        make()
        make("install")
        if sys.platform == 'darwin':
            fix_darwin_install_name(prefix.lib)
