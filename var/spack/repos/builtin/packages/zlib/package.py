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


# Although zlib comes with a configure script, it does not use Autotools
# The AutotoolsPackage causes zlib to fail to build with PGI
class Zlib(Package):
    """A free, general-purpose, legally unencumbered lossless
       data-compression library."""

    homepage = "http://zlib.net"
    # URL must remain http:// so Spack can bootstrap curl
    url = "http://zlib.net/fossils/zlib-1.2.11.tar.gz"

    version('1.2.11', '1c9f62f0778697a09d36121ead88e08e')
    # Due to the bug fixes, any installations of 1.2.9 or 1.2.10 should be
    # immediately replaced with 1.2.11.
    version('1.2.8', '44d667c142d7cda120332623eab69f40')

    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')
    variant('shared', default=True,
            description='Enables the build of shared libraries.')

    def setup_environment(self, spack_env, run_env):
        if '+pic' in self.spec:
            spack_env.set('CFLAGS', self.compiler.pic_flag)

    def install(self, spec, prefix):
        config_args = []
        if '~shared' in spec:
            config_args.append('--static')
        configure('--prefix={0}'.format(prefix), *config_args)

        make()
        if self.run_tests:
            make('check')
        make('install')
