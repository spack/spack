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


class AppleCctools(MakefilePackage):
    """apple-cctools: Binary and cross-compilation tools for Apple

    cctools contains the source to Apple's build toolchain, and is the
    Apple analogue to binutils, libtool"""

    homepage = "https://opensource.apple.com/source/cctools/"
    url      = "https://opensource.apple.com/tarballs/cctools/cctools-895.tar.gz"

    version('895', '6bf19547c93c6f0f921de04eabde2ae0')

    variant('lto', default=False,
            description='Enable LTO support (requires llvm@3.4:)')

    # NOTE: This package was tested on Mac OS X Sierra (10.12); it
    # will probably work for 10.13, but may not for earlier versions
    # of OS X. However, the MacPorts and Homebrew versions of this
    # package include additional code to handle these cases, so it's
    # possible an interested developer with access to earlier versions
    # of OS X could get this additional code up and running.

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

    # Patch to uncomment and apply if OS X 10.11 or earlier; if users
    # need support for OS X 10.11 (untested)
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

    def edit(self, spec, prefix):
        # Add MacPorts post-patch edits from their cctools package here;
        # MacPorts' `reinplace` command calls `sed -e`, so Python
        # equivalents must be reverse-engineered
        makefile = FileFilter('Makefile')
        makefile.filter(r'^SUBDIRS_32\s=\sld', 'SUBDIRS_32 = ')

        # The substitutions in this block should obviate the need to
        # move too many files (which is what Homebrew does). Many of these
        # were detemined by looking at Makefiles, followed by trial and error
        makefile_list = glob.glob('*/Makefile') + ['Makefile']
        for f in makefile_list:
            ff = FileFilter(f)
            ff.filter('^DSTROOT\s=\s.*',
                      'DSTROOT = {0}'.format(self.spec.prefix))
            ff.filter('^BINDIR\s=\s.*', 'BINDIR = /bin')
            ff.filter('^MANDIR\s=\s.*', 'MANDIR = /man')
            ff.filter('^LOCMANDIR\s=\s.*', 'LOCMANDIR = /man')
            ff.filter('^EFIMANDIR\s=\s.*', 'EFIMANDIR = /man')
            ff.filter('^USRBINDIR\s=\s.*', 'USRBINDIR = /bin')
            ff.filter('^LOCBINDIR\s=\s.*', 'LOCBINDIR = /bin')
            ff.filter('^LOCLIBDIR\s=\s.*', 'LOCLIBDIR = /lib')
            ff.filter('^LIBDIR\s=\s.*', 'LIBDIR = /lib')
            ff.filter('^EFIBINDIR\s=\s.*', 'EFIBINDIR = /bin')
            ff.filter(r'/Local/Developer/System', self.spec.prefix + r'/lib')
            ff.filter(r'/usr/local/lib/system', self.spec.prefix + r'/lib')
            ff.filter(r'/usr/libexec/DeveloperTools', r'/libexec')
            ff.filter(r'/usr/include', r'/include')
            ff.filter(r'/usr/libexec', r'/libexec')
            ff.filter(r'/usr/local/include', r'/include')
            ff.filter(r'/usr/local', r'/share')

            # Don't strip installed binaries
            ff.filter(r'(install.*)\-s ', r'\1')

        if spec.satisfies('+lto'):
            lto_c = FileFilter(join_path('libstuff', 'lto.c'))
            lto_c.filter('@@LLVM_LIBDIR', spec['llvm'].prefix.lib)

    def build(self, spec, prefix):
        #  Do Macports 'post-extract' steps from their cctools package
        #  here to get past prune_trie error
        cp = which('cp')
        cp(join_path('ld64', 'src', 'other', 'PruneTrie.cpp'),
           join_path('misc', 'PruneTrie.cpp'))
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
                     'RAW_DSTROOT={0}'.format(self.spec.prefix),
                     'CPPFLAGS=-I{0} -I{1} -I{2} -I. -I..'.format(
                         join_path(abspath, 'ld64', 'src', 'abstraction'),
                         join_path(abspath, 'ld64', 'src', 'other'),
                         join_path(abspath, 'include')),
                     'RC_CFLAGS={0}'.format(my_cflags),
                     'SYSTEMDIR=/libexec']

        # From Homebrew: fixes build with gcc-4.2:
        # https://trac.macports.org/ticket/43745
        # make_args.append('SDK=-std=gnu99') is supposed to fix build
        # issues with gcc-4.2, but passing this flag also passes
        # `-std=gnu99` to the C++ compiler, which is an error, at
        # least for LLVM.
        make_args.append('SDK=')

        # Assume CPU is Intel; if CPU not Intel, must add ppc arch;
        # see commented line below
        make_args.append('RC_ARCHS=i386 x86_64')
        # make_args.append('RC_ARCHS="ppc i386 x86_64"')  # if CPU not Intel
        make('install_tools', *make_args)

    # Clean up paths that are superfluous after all of the path hacking above
    def install(self, spec, prefix):
        remove_linked_tree(self.spec.prefix.usr)
        remove_linked_tree(self.spec.prefix.libexec)
