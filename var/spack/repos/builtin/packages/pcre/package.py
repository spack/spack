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


class Pcre(Package):
    """The PCRE package contains Perl Compatible Regular Expression
       libraries. These are useful for implementing regular expression
       pattern matching using the same syntax and semantics as Perl 5."""
    homepage = "http://www.pcre.org"""
    url      = "https://ftp.pcre.org/pub/pcre/pcre-8.36.tar.bz2"

    version('8.39', 'e3fca7650a0556a2647821679d81f585')
    version('8.38', '00aabbfe56d5a48b270f999b508c5ad2')

    patch("intel.patch", when='@8.38')

    variant('utf', default=True,
            description='Enable support for UTF-8/16/32, '
            'incompatible with EBCDIC.')

    def install(self, spec, prefix):
        configure_args = ['--prefix=%s' % prefix]
        if '+utf' in spec:
            configure_args.append('--enable-utf')
            configure_args.append('--enable-unicode-properties')

        configure(*configure_args)
        make()
        make("install")
