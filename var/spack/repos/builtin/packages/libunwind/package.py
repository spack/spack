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


class Libunwind(AutotoolsPackage):
    """A portable and efficient C programming interface (API) to determine
       the call-chain of a program."""

    homepage = "http://www.nongnu.org/libunwind/"
    url      = "http://download.savannah.gnu.org/releases/libunwind/libunwind-1.1.tar.gz"

    version('1.3-rc1', 'f09b670de5db6430a3de666e6aed60e3')
    version('1.2.1', '06ba9e60d92fd6f55cd9dadb084df19e', preferred=True)
    version('1.1', 'fb4ea2f6fbbe45bf032cd36e586883ce')

    variant('xz', default=False,
            description='Support xz (lzma) compressed symbol tables.')

    depends_on('xz', type='link', when='+xz')

    conflicts('platform=darwin',
              msg='Non-GNU libunwind needs ELF libraries Darwin does not have')

    provides('unwind')

    def configure_args(self):
        spec = self.spec
        args = []

        if '+xz' in spec:
            args.append('--enable-minidebuginfo')
        else:
            args.append('--disable-minidebuginfo')

        return args
