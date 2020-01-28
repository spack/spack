# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libunwind(AutotoolsPackage):
    """A portable and efficient C programming interface (API) to determine
       the call-chain of a program."""

    homepage = "http://www.nongnu.org/libunwind/"
    url      = "http://download.savannah.gnu.org/releases/libunwind/libunwind-1.1.tar.gz"
    git      = "https://github.com/libunwind/libunwind"

    version('develop', branch='master')
    version('2018.10.12', commit='f551e16213c52169af8bda554e4051b756a169cc')
    version('1.3-rc1', sha256='e40f49dcbfdea3f4d15fa555fe68958e69a3f410aacf1ec46fd86aeced699773')
    version('1.2.1', sha256='3f3ecb90e28cbe53fba7a4a27ccce7aad188d3210bb1964a923a731a27a75acb', preferred=True)
    version('1.1', sha256='9dfe0fcae2a866de9d3942c66995e4b460230446887dbdab302d41a8aee8d09a')

    variant('xz', default=False,
            description='Support xz (lzma) compressed symbol tables.')

    # The libunwind releases contain the autotools generated files,
    # but the git repo snapshots do not.
    depends_on('autoconf', type='build', when='@2018:')
    depends_on('automake', type='build', when='@2018:')
    depends_on('libtool',  type='build', when='@2018:')
    depends_on('m4',       type='build', when='@2018:')

    depends_on('xz', type='link', when='+xz')

    conflicts('platform=darwin',
              msg='Non-GNU libunwind needs ELF libraries Darwin does not have')

    provides('unwind')

    flag_handler = AutotoolsPackage.build_system_flags

    def configure_args(self):
        spec = self.spec
        args = []

        if '+xz' in spec:
            args.append('--enable-minidebuginfo')
        else:
            args.append('--disable-minidebuginfo')

        return args
