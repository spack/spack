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


class Zfp(Package):
    """zfp is an open source C library for compressed floating-point arrays
       that supports very high throughput read and write random acces,
       target error bounds or bit rates.  Although bit-for-bit lossless
       compression is not always possible, zfp is usually accurate to
       within machine epsilon in near-lossless mode, and is often orders
       of magnitude more accurate than other lossy compressors. Versions
       of zfp 0.5.1 or newer also support compression of integer data.
    """

    homepage = "http://computation.llnl.gov/projects/floating-point-compression"
    url      = "http://computation.llnl.gov/projects/floating-point-compression/download/zfp-0.5.1.tar.gz"
    list_url = "http://computation.llnl.gov/projects/floating-point-compression/download"
    list_depth = 1

    version('0.5.1', '0ed7059a9b480635e0dd33745e213d17')
    version('0.5.0', '2ab29a852e65ad85aae38925c5003654')

    variant('bswtuint8', default=False,
        description='Build with bit stream word type of uint8')

    def edit(self, spec, prefix):
        config_file = FileFilter('Config')

        if '+bswtunit8' in self.spec:
            config_file.filter('#DEFS += -DBIT_STREAM_WORD_TYPE=uint8)','DEFS += -DBIT_STREAM_WORD_TYPE=uint8')

    def install(self, spec, prefix):
        make("shared")

        zfp_incdir = 'inc'
        if spec.satisfies('@0.5.1:'):
            zfp_incdir = 'include'

        # No install provided
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        install('lib/libzfp.so', prefix.lib)
        install('%s/zfp.h'%zfp_incdir, prefix.include)
        install('%s/bitstream.h'%zfp_incdir, prefix.include)
        if spec.satisfies('@0.5.1:'):
            mkdirp('%s/zfp'%prefix.include)
            install('%s/zfp/system.h'%zfp_incdir, '%s/zfp'%prefix.include)
            install('%s/zfp/types.h'%zfp_incdir, '%s/zfp'%prefix.include)
        else:
            install('%s/types.h'%zfp_incdir, prefix.include)
            install('%s/system.h'%zfp_incdir, prefix.include)
