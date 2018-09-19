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


class Xqilla(AutotoolsPackage):
    """XQilla is an XQuery and XPath 2 library and command line utility
    written in C++, implemented on top of the Xerces-C library."""

    homepage = "http://xqilla.sourceforge.net/HomePage"
    url      = "https://downloads.sourceforge.net/project/xqilla/XQilla-2.3.3.tar.gz"

    version('2.3.3', '8ece20348687b6529bb934c17067803c')

    variant('debug', default=False, description='Build a debugging version.')
    variant('shared', default=True, description='Build shared libraries.')

    depends_on('xerces-c')

    def configure_args(self):
        args = ['--with-xerces={0}'.format(self.spec['xerces-c'].prefix)]

        if '+shared' in self.spec:
            args.extend(['--enable-shared=yes',
                         '--enable-static=no'])
        else:
            args.extend(['--enable-shared=no',
                         '--enable-static=yes',
                         '--with-pic'])

        if '+debug' in self.spec:
            args.append('--enable-debug')

        return args
