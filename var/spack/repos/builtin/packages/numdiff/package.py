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


class Numdiff(AutotoolsPackage):
    """Numdiff is a little program that can be used to compare putatively
    similar files line by line and field by field, ignoring small numeric
    differences or/and different numeric formats."""

    homepage  = 'https://www.nongnu.org/numdiff'
    url       = 'http://nongnu.askapache.com/numdiff/numdiff-5.8.1.tar.gz'

    version('5.8.1', 'a295eb391f6cb1578209fc6b4f9d994e')

    variant('nls', default=False,
            description="Enable Natural Language Support")
    variant('gmp', default=False,
            description="Use GNU Multiple Precision Arithmetic Library")

    depends_on('gettext', when='+nls')
    depends_on('gmp', when='+gmp')

    def configure_args(self):
        spec = self.spec
        args = []
        if '+nls' in spec:
            args.append('--enable-nls')
        else:
            args.append('--disable-nls')

        if '+gmp' in spec:
            # compile with -O0 as per upstream known issue with optimization
            # and GMP; https://launchpad.net/ubuntu/+source/numdiff/+changelog
            # http://www.nongnu.org/numdiff/#issues
            # keep this variant off by default as one still encounter
            # GNU MP: Cannot allocate memory (size=2305843009206983184)
            args.extend([
                '--enable-gmp',
                'CFLAGS=-O0'
            ])
        else:
            args.append('--disable-gmp')

        return args
