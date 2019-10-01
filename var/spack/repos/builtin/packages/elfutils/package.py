# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import os.path


class Elfutils(AutotoolsPackage):
    """elfutils is a collection of various binary tools such as
    eu-objdump, eu-readelf, and other utilities that allow you to
    inspect and manipulate ELF files. Refer to Table 5.Tools Included
    in elfutils for Red Hat Developer for a complete list of binary
    tools that are distributed with the Red Hat Developer Toolset
    version of elfutils."""

    homepage = "https://fedorahosted.org/elfutils/"
    url      = "https://sourceware.org/elfutils/ftp/0.176/elfutils-0.176.tar.bz2"
    list_url = "https://sourceware.org/elfutils/ftp"
    list_depth = 1

    version('0.176', '077e4f49320cad82bf17a997068b1db9')
    version('0.175', '9a02b0382b78cc2d515fb950275d4c02')
    version('0.174', '48bec24c0c8b2c16820326956dff9378')
    version('0.173', '35decb1ebfb90d565e4c411bee4185cc')
    version('0.170', '03599aee98c9b726c7a732a2dd0245d5')
    version('0.168', '52adfa40758d0d39e5d5c57689bf38d6')
    version('0.163', '77ce87f259987d2e54e4d87b86cbee41')

    # Libraries for reading compressed DWARF sections.
    variant('bzip2', default=False,
            description='Support bzip2 compressed sections.')
    variant('xz', default=False,
            description='Support xz (lzma) compressed sections.')

    # Native language support from libintl.
    variant('nls', default=True,
            description='Enable Native Language Support.')

    depends_on('bzip2', type='link', when='+bzip2')
    depends_on('xz',    type='link', when='+xz')
    depends_on('zlib',  type='link')
    depends_on('gettext', when='+nls')
    depends_on('m4',    type='build')

    conflicts('%gcc@7.2.0:', when='@0.163')

    provides('elf@1')

    # Elfutils uses nested functions in C code, which is implemented
    # in gcc, but not in clang. C code compiled with gcc is
    # binary-compatible with clang, so it should be possible to build
    # elfutils with gcc, and then link it to clang-built libraries.
    conflicts('%clang')

    # Elfutils uses -Wall and we don't want to fail the build over a
    # stray warning.
    def patch(self):
        files = glob.glob(os.path.join('*', 'Makefile.in'))
        filter_file('-Werror', '', *files)

    flag_handler = AutotoolsPackage.build_system_flags

    def configure_args(self):
        spec = self.spec
        args = []

        if '+bzip2' in spec:
            args.append('--with-bzlib=%s' % spec['bzip2'].prefix)
        else:
            args.append('--without-bzlib')

        if '+xz' in spec:
            args.append('--with-lzma=%s' % spec['xz'].prefix)
        else:
            args.append('--without-lzma')

        # zlib is required
        args.append('--with-zlib=%s' % spec['zlib'].prefix)

        if '+nls' in spec:
            # configure doesn't use LIBS correctly
            args.append('LDFLAGS=-Wl,--no-as-needed -L%s -lintl' %
                        spec['gettext'].prefix.lib)
        else:
            args.append('--disable-nls')

        return args

    # Install elf.h to include directory.
    @run_after('install')
    def install_elfh(self):
        install(join_path('libelf', 'elf.h'), self.prefix.include)

    # Provide location of libelf.so to match libelf.
    @property
    def libs(self):
        return find_libraries('libelf', self.prefix, recursive=True)
