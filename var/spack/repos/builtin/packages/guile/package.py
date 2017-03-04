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


class Guile(Package):
    """Guile is the GNU Ubiquitous Intelligent Language for Extensions,
    the official extension language for the GNU operating system."""

    homepage = "https://www.gnu.org/software/guile/"
    url      = "https://ftp.gnu.org/gnu/guile/guile-2.0.11.tar.gz"

    version('2.0.11', 'e532c68c6f17822561e3001136635ddd')

    variant('readline', default=True, description='Use the readline library')

    depends_on('gmp@4.2:')
    depends_on('gettext')
    depends_on('libtool@1.5.6:')
    depends_on('libunistring@0.9.3:')
    depends_on('bdw-gc@7.0:')
    depends_on('libffi')
    depends_on('readline', when='+readline')
    depends_on('pkg-config', type='build')

    def install(self, spec, prefix):
        config_args = [
            '--prefix={0}'.format(prefix),
            '--with-libunistring-prefix={0}'.format(
                spec['libunistring'].prefix),
            '--with-libltdl-prefix={0}'.format(spec['libtool'].prefix),
            '--with-libgmp-prefix={0}'.format(spec['gmp'].prefix),
            '--with-libintl-prefix={0}'.format(spec['gettext'].prefix)
        ]

        if '+readline' in spec:
            config_args.append('--with-libreadline-prefix={0}'.format(
                spec['readline'].prefix))
        else:
            config_args.append('--without-libreadline-prefix')

        configure(*config_args)

        make()
        make('check')
        make('install')
