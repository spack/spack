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


class Ndiff(Package):
    """The ndiff tool is a binary utility that compares putatively similar
       files while ignoring small numeric differernces. This utility is
       most often used to compare files containing a lot of
       floating-point numeric data that may be slightly different due to
       numeric error.

    """

    homepage = "http://ftp.math.utah.edu/pub/ndiff/"
    url      = "http://ftp.math.utah.edu/pub/ndiff/ndiff-2.00.tar.gz"

    version('2.00', '885548b4dc26e72c5455bebb5ba6c16d')
    version('1.00', 'f41ffe5d12f36cd36b6311acf46eccdc')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        mkdirp(prefix.bin)
        mkdirp('%s/lib' % prefix.share)

        make('install-exe', 'install-shrlib')
