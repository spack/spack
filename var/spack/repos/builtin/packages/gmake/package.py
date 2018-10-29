# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gmake(AutotoolsPackage):
    """GNU Make is a tool which controls the generation of executables and
    other non-source files of a program from the program's source files."""

    homepage = "https://www.gnu.org/software/make/"
    url      = "https://ftpmirror.gnu.org/make/make-4.2.1.tar.gz"

    version('4.2.1', '7d0dcb6c474b258aab4d54098f2cf5a7')
    version('4.0',   'b5e558f981326d9ca1bfdb841640721a')

    variant('guile', default=False, description='Support GNU Guile for embedded scripting')
    variant('nls', default=True, description='Enable Native Language Support')

    depends_on('gettext', when='+nls')
    depends_on('guile', when='+guile')

    build_directory = 'spack-build'

    patch('https://src.fedoraproject.org/rpms/make/raw/519a7c5bcbead22e6ea2d2c2341d981ef9e25c0d/f/make-4.2.1-glob-fix-2.patch', level=1, sha256='fe5b60d091c33f169740df8cb718bf4259f84528b42435194ffe0dd5b79cd125', when='@4.2.1')
    patch('https://src.fedoraproject.org/rpms/make/raw/519a7c5bcbead22e6ea2d2c2341d981ef9e25c0d/f/make-4.2.1-glob-fix-3.patch', level=1, sha256='ca60bd9c1a1b35bc0dc58b6a4a19d5c2651f7a94a4b22b2c5ea001a1ca7a8a7f', when='@:4.2.1')

    def configure_args(self):
        args = []

        if '+guile' in self.spec:
            args.append('--with-guile')
        else:
            args.append('--without-guile')

        if '+nls' in self.spec:
            args.append('--enable-nls')
        else:
            args.append('--disable-nls')

        return args

    @run_after('install')
    def symlink_gmake(self):
        with working_dir(self.prefix.bin):
            symlink('make', 'gmake')
