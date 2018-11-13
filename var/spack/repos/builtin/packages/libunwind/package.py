# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
