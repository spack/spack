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
    """Guile is designed to help programmers create flexible applications
    that can be extended by users or other programmers with plug-ins,
    modules, or scripts."""

    homepage = "https://www.gnu.org/software/guile/"
    url      = "ftp://ftp.gnu.org/gnu/guile/guile-2.0.11.tar.gz"

    version('2.0.11', 'e532c68c6f17822561e3001136635ddd')

    variant('readline', default=True, description='Use the readline library')

    depends_on('gmp@4.2:')
    depends_on('libiconv')
    depends_on('gettext')
    depends_on('libtool@1.5.6:')
    depends_on('libunistring@0.9.3:')
    depends_on('gc@7.0:')
    depends_on('libffi')
    depends_on('readline', when='+readline')
    depends_on('pkg-config')

    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix))

        make()
        make('install')
