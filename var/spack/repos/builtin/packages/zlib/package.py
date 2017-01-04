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
from os import environ


class Zlib(AutotoolsPackage):
    """A free, general-purpose, legally unencumbered lossless
       data-compression library."""

    homepage = "http://zlib.net"
    url = "https://github.com/madler/zlib/archive/v1.2.10.tar.gz"

    version('1.2.10', 'ee405a38e77b3ffb5c7ff72aa074df1a')
    version('1.2.9', 'e727f2484bf2a4eff2fc6b5f2e138ae2')
    version('1.2.8', '1eabf2698dc49f925ce0ffb81397098f')
    version('1.2.7.3', '202e813c183f91578f0b35787ab4cf5a')
    version('1.2.7.2', 'afd13ef1255c1042c388a1ef8cb314d6')
    version('1.2.7.1', '0a05b3a3955fea5b477c04093ea00fc0')
    version('1.2.7', 'cbcc3eddd76da39170e4bf9ab93d02fd')
    version('1.2.6.1', 'f64045cd2f229a558f060367cc197c60')
    version('1.2.6', 'b778e8a8add5281b52900a9a1c3ffa63')
    version('1.2.5.3', '554651e0f60e2bc9f40b03e3b18e41f3')

    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')

    def configure(self, spec, prefix):

        if '+pic' in spec:
            environ['CFLAGS'] = self.compiler.pic_flag

        config_args = ['--prefix', prefix]
        configure(*config_args)
