# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Valgrind(AutotoolsPackage):
    """An instrumentation framework for building dynamic analysis.

    There are Valgrind tools that can automatically detect many memory
    management and threading bugs, and profile your programs in
    detail. You can also use Valgrind to build new tools.

    Valgrind is Open Source / Free Software, and is freely available
    under the GNU General Public License, version 2.
    """
    homepage = "http://valgrind.org/"
    url      = "https://sourceware.org/pub/valgrind/valgrind-3.13.0.tar.bz2"
    git      = "git://sourceware.org/git/valgrind.git"

    version('develop', branch='master')
    version('3.15.0', sha256='417c7a9da8f60dd05698b3a7bc6002e4ef996f14c13f0ff96679a16873e78ab1')
    version('3.14.0', '74175426afa280184b62591b58c671b3')
    version('3.13.0', '817dd08f1e8a66336b9ff206400a5369')
    version('3.12.0', '6eb03c0c10ea917013a7622e483d61bb')
    version('3.11.0', '4ea62074da73ae82e0162d6550d3f129')
    version('3.10.1', '60ddae962bc79e7c95cfc4667245707f')
    version('3.10.0', '7c311a72a20388aceced1aa5573ce970')

    variant('mpi', default=True,
            description='Activates MPI support for valgrind')
    variant('boost', default=True,
            description='Activates boost support for valgrind')
    variant('only64bit', default=True,
            description='Sets --enable-only64bit option for valgrind')
    variant('ubsan', default=True,
            description='Activates ubsan support for valgrind')

    conflicts('+ubsan', when='platform=darwin %clang',
              msg="""
Cannot build libubsan with clang on macOS.
Otherwise with (Apple's) clang there is a linker error:
clang: error: unknown argument: '-static-libubsan'
""")
    depends_on('mpi', when='+mpi')
    depends_on('boost', when='+boost')

    depends_on("autoconf", type='build', when='@develop')
    depends_on("automake", type='build', when='@develop')
    depends_on("libtool", type='build', when='@develop')

    # Apply the patch suggested here:
    # http://valgrind.10908.n7.nabble.com/Unable-to-compile-on-Mac-OS-X-10-11-td57237.html
    patch('valgrind_3_12_0_osx.patch', when='@3.12.0 platform=darwin')

    def configure_args(self):
        spec = self.spec
        options = []
        if spec.satisfies('+ubsan'):
            options.append('--enable-ubsan')
        if spec.satisfies('+only64bit'):
            options.append('--enable-only64bit')

        if sys.platform == 'darwin':
            options.append('--build=amd64-darwin')
        return options
