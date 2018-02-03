##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import glob
import re


class AppleCctools(MakefilePackage):
    """apple-cctools: Binary and cross-compilation tools for Apple

    cctools contains the source to Apple's build toolchain, and is the
    Apple analogue to binutils, libtool"""

    homepage = "https://opensource.apple.com/source/cctools/"
    url      = "https://opensource.apple.com/tarballs/cctools/cctools-895.tar.gz"

    version('895', '6bf19547c93c6f0f921de04eabde2ae0')

    variant('lto', default=False,
            description='Enable LTO support (requires llvm@3.4:)')

    # Patches from MacPorts. See source at
    # https://github.com/macports/macports-ports/tree/master/devel/cctools/files
    # See MacPorts package at
    # https://github.com/macports/macports-ports/tree/master/devel/cctools/files
    # See Homebrew package at
    # https://github.com/Homebrew/homebrew-core/blob/master/Formula/cctools.rb
    patch('cctools-829-lto.patch', level=0)
    patch('PR-37520.patch', level=0)
    patch('cctools-839-static-dis_info.patch', level=0)
    patch('PR-12400897.patch', level=0)
    patch('cctools-862-prunetrie.patch', level=0)
    patch('cctools-895-big_endian.patch', level=0)
    patch('cctools-895-OFILE_LLVM_BITCODE.patch', level=0)
    patch('not-clang.patch', level=0)

    # Patch from Homebrew
#    patch('libtool-no-lto.diff', level=1, when='~lto')

    # Patch to apply if OS X 10.11 or earlier; if users need support
    # for OS X 10.11
    # patch('snowleopard-strnlen.patch', level=0)

    depends_on('llvm@3.4:', when='+lto')

    # Homebrew does not build apple-cctools in parallel
    parallel = False

    # Vend in ld64, like MacPorts; in recent OS X releases, Apple's ld is
    # really ld64, which can be seen by typing `ld --help` and looking at
    # the error message:
    # "ld64: For information on command line options please use 'man ld'";
    # of course, without building and installing via source, `man ld` returns
    # "No manual entry for ld".
    resource(name='ld64', url='http://opensource.apple.com/tarballs/ld64/ld64-274.2.tar.gz',
             md5='cde416fd1d96fa41a0bf0ea034428e36',
             placement='ld64')

#     def setup_environment(self, spack_env, run_env):
#         # Add MacPorts configure.cflags-append and cppflags-append
#         # directives here
#         abspath = self.stage.source_path
#         spack_env.append_flags('CPPFLAGS',
#                                '-I{0} -I{1} -I{2}'.format(
#                                    join_path(abspath, 'ld64', 'src', 'abstraction'),
#                                    join_path(abspath, 'ld64', 'src', 'other'),
#                                    join_path(abspath, 'include')))
#         spack_env.append_flags('CFLAGS', '-std=gnu99')
#         spack_env.append_flags('CXXFLAGS', '-O2 -g')
# #        spack_env.append_flags('CFLAGS', '-std=gnu99')

    def edit(self, spec, prefix):
        # Add MacPorts post-patch edits from their cctools package here;
        # MacPorts' `reinplace` command calls `sed -e`
        makefile = FileFilter('Makefile')
        makefile.filter(r'^SUBDIRS_32\s=\sld', 'SUBDIRS_32 = ')
        #makefile.filter(r'^COMMON_SUBDIRS\s/ ld ', ' ')

        # The substitutions in this block should obviate the need to
        # move too many files (which is what Homebrew does)
        makefile_list = glob.glob('{*/,}Makefile')
        for f in makefile_list:
            ff = FileFilter(f)
            ff.filter('^DSTROOT\s=\s.*', 'DSTROOT = {0}'.format(self.spec.prefix))
            ff.filter('^BINDIR\s=\s.*', 'BINDIR = /bin')
            ff.filter('^MANDIR\s=\s.*', 'MANDIR = /man')
            ff.filter('^LOCMANDIR\s=\s.*', 'LOCMANDIR = /man')
            ff.filter('^EFIMANDIR\s=\s.*', 'EFIMANDIR = /man')
            ff.filter('^USRBINDIR\s=\s.*', 'USRBINDIR = /bin')
            ff.filter('^LOCBINDIR\s=\s.*', 'LOCBINDIR = /bin')
            ff.filter('^LOCLIBDIR\s=\s.*', 'LOCLIBDIR = /lib')
            ff.filter('^LIBDIR\s=\s.*', 'LIBDIR = /lib')
            ff.filter('^EFIBINDIR\s=\s.*', 'EFIBINDIR = /bin')
            ff.filter('/Local/Developer/System', self.spec.prefix + '/lib')
            ff.filter('/usr/local/lib/system', self.spec.prefix + '/lib')
            ff.filter('/usr/libexec/DeveloperTools', '/libexec')

            # Don't strip installed binaries
            ff.filter(r'(install .*)-s ',r'\1')

        if spec.satisfies('+lto'):
            lto_c = FileFilter(join_path('libstuff', 'lto.c'))
            lto_c.filter('@@LLVM_LIBDIR', spec['llvm'].prefix.lib)

    def build(self, spec, prefix):
        #  Do Macports 'post-extract' steps from their cctools package
        #  here to get past prune_trie error
        cp = which('cp')
        cp(join_path('ld64', 'src', 'other', 'PruneTrie.cpp'), join_path('misc', 'PruneTrie.cpp'))
        touch = which('touch')
        touch(join_path('ld64', 'src', 'abstraction', 'configure.h'))

        lto_flag = '-DLTO_SUPPORT' if spec.satisfies('+lto') else ''
        abspath = self.stage.source_path
        my_cflags = '-I{0} -I{1} -I{2} -I. -I..'.format(
            join_path(abspath, 'ld64', 'src', 'abstraction'),
            join_path(abspath, 'ld64', 'src', 'other'),
            join_path(abspath, 'include')) + ' -Os -g -Wall'

        make_args = ['RC_ProjectSourceVersion={0}'.format(spec.version),
                     'USE_DEPENDENCY_FILE=NO',
                     'CC={0}'.format(self.compiler.cc),
                     'CXX={0}'.format(self.compiler.cxx),
                     'LTO={0}'.format(lto_flag),
                     'TRIE=',
                     'RC_OS=macos',
                     'DSTROOT={0}'.format(self.spec.prefix),
                     'RAW_DSTROOT={0}'.format(self.spec.prefix),
#                     'CXXFLAGS=-Os -g -Wall',
#                     'CFLAGS=-Os -g -Wall',
                     'CPPFLAGS=-I{0} -I{1} -I{2} -I. -I..'.format(
                                   join_path(abspath, 'ld64', 'src', 'abstraction'),
                                   join_path(abspath, 'ld64', 'src', 'other'),
                                   join_path(abspath, 'include')),
                     'RC_CFLAGS={0}'.format(my_cflags),
                     'BINDIR=/bin',
                     'MANDIR=/man',
                     'LOCMANDIR=/man',
                     'EFIMANDIR=/man',
                     'USRBINDIR=/bin',
                     'LOCBINDIR=/bin',
                     'LOCLIBDIR=/lib',
                     'LIBDIR=/lib',
                     'EFIBINDIR=/bin',
                     'SYSTEMDIR=/libexec'
        ]

        # From Homebrew: fixes build with gcc-4.2: https://trac.macports.org/ticket/43745
#        make_args.append('SDK=-std=gnu99')
        make_args.append('SDK=')

        # Assume CPU is Intel; if CPU not Intel, must add ppc arch; see commented line below
        make_args.append('RC_ARCHS=i386 x86_64')
        # make_args.append('RC_ARCHS="ppc i386 x86_64"')  # if CPU not Intel
        make('install_tools', *make_args)
#        make('-e', 'install_tools', *make_args)  # want env vars passed into sub-makes

    def install(self, spec, prefix):
        pass
        # install_tree(prefix.usr.local, prefix)
        # install_tree(prefix.usr.local.man, prefix.man)
        # install_tree(prefix.usr.bin, prefix.bin)
        # install_tree(usr_include_mach_o,include_mach_o)
        # install_tree(prefix.usr.share.man.man1, prefix.man.man1)
        # install_tree(prefix.usr.share.man.man3, prefix.man.man3)
        # install_tree(prefix.usr.share.man.man5, prefix.man.man5)

        # Applies to OS X version >= Snow Leopard (10.6?);
        # need to use join_path because "as" is a Python keyword
        #libexec_as = join_path(prefix.libexec, 'as')
        #usr_libexec_as = join_path(prefix.usr.libexec, 'as')
        #mkdirp(libexec_as)
        #install_tree(usr_libexec_as, libexec_as)

        # If OS X version < Snow Leopard, would execute:
        # libexec_gcc_darwin = prefix.libexec.gcc.darwin
        # usr_libexec_gcc_darwin = prefix.usr.libexec.gcc.darwin
        # mkdirp(prefix.libexec.gcc.darwin)
        # install_tree(usr_libexec_gcc_darwin, libexec_gcc_darwin)
        # install_tree(prefix.share, join_path(prefix.usr.share, 'gprof.*'))

        #pass
        # mkdirp(prefix)
        # mkdirp(prefix.man)
        # mkdirp(prefix.bin)
        # mkdirp(prefix.lib)
        # mkdirp(prefix.libexec)
        # mkdirp(prefix.man1)
        # mkdirp(include_mach_o)
        # mkdirp(prefix.man1)
        # mkdirp(prefix.man3)
        # mkdirp(prefix.man5)
        # make('install_tools', *make_args)
