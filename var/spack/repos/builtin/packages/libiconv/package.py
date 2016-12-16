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
import shutil


class Libiconv(AutotoolsPackage):
    """GNU libiconv provides an implementation of the iconv() function
    and the iconv program for character set conversion."""

    homepage = "https://www.gnu.org/software/libiconv/"
    url      = "http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.14.tar.gz"

    version('1.14', 'e34509b1623cec449dfeb73d7ce9c6c6')

    # We cannot set up a warning for gets(), since gets() is not part
    # of C11 any more and thus might not exist.
    patch("gets.patch")

    def configure_args(self):
        args = ['--enable-extra-encodings']

        # A hack to patch config.guess in the libcharset sub directory
        shutil.copyfile('./build-aux/config.guess',
                        'libcharset/build-aux/config.guess')
        return args
