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
from spack.operating_systems.mac_os import macos_version
from llnl.util import tty

import glob
import os
import sys


class Gcc(AutotoolsPackage):
    """The GNU Compiler Collection includes front ends for C, C++, Objective-C,
    Fortran, Ada, and Go, as well as libraries for these languages."""

    homepage = 'https://gcc.gnu.org'
    url      = 'https://ftpmirror.gnu.org/gcc/gcc-7.1.0/gcc-7.1.0.tar.bz2'
    list_url = 'http://ftp.gnu.org/gnu/gcc/'
    list_depth = 1

    version('8.2.0', '64898a165f67e136d802a92e7633bf1b06c85266027e52127ea025bf5fc2291b5e858288aac0bdba246e6cdf7c6ec88bc8e0e7f3f6f1985f4297710cafde56ed')
    version('8.1.0', '65f7c65818dc540b3437605026d329fc')
    version('7.3.0', 'be2da21680f27624f3a87055c4ba5af2')
    version('7.2.0', 'ff370482573133a7fcdd96cd2f552292')
    version('7.1.0', '6bf56a2bca9dac9dbbf8e8d1036964a8')
    version('6.4.0', '11ba51a0cfb8471927f387c8895fe232')
    version('6.3.0', '677a7623c7ef6ab99881bc4e048debb6')
    version('6.2.0', '9768625159663b300ae4de2f4745fcc4')
    version('6.1.0', '8fb6cb98b8459f5863328380fbf06bd1')
    version('5.5.0', '0f70424213b4a1113c04ba66ddda0c1f')
    version('5.4.0', '4c626ac2a83ef30dfb9260e6f59c2b30')
    version('5.3.0', 'c9616fd448f980259c31de613e575719')
    version('5.2.0', 'a51bcfeb3da7dd4c623e27207ed43467')
    version('5.1.0', 'd5525b1127d07d215960e6051c5da35e')
    version('4.9.4', '87c24a4090c1577ba817ec6882602491')
    version('4.9.3', '6f831b4d251872736e8e9cc09746f327')
    version('4.9.2', '4df8ee253b7f3863ad0b86359cd39c43')
    version('4.9.1', 'fddf71348546af523353bd43d34919c1')
    version('4.8.5', '80d2c2982a3392bb0b89673ff136e223')
    version('4.8.4', '5a84a30839b2aca22a2d723de2a626ec')
    version('4.7.4', '4c696da46297de6ae77a82797d2abe28')
    version('4.6.4', 'b407a3d1480c11667f293bfb1f17d1a4')
    version('4.5.4', '27e459c2566b8209ab064570e1b378f7')

    # We specifically do not add 'all' variant here because:
    # (i) Ada, Go, Jit, and Objective-C++ are not default languages.
    # In that respect, the name 'all' is rather misleading.
    # (ii) Languages other than c,c++,fortran are prone to configure bug in GCC
    # For example, 'java' appears to ignore custom location of zlib
    # (iii) meaning of 'all' changes with GCC version, i.e. 'java' is not part
    # of gcc7. Correctly specifying conflicts() and depends_on() in such a
    # case is a PITA.
    variant('languages',
            default='c,c++,fortran',
            values=('ada', 'brig', 'c', 'c++', 'fortran',
                    'go', 'java', 'jit', 'lto', 'objc', 'obj-c++'),
            multi=True,
            description='Compilers and runtime libraries to build')
    variant('binutils',
            default=False,
            description='Build via binutils')
    variant('piclibs',
            default=False,
            description='Build PIC versions of libgfortran.a and libstdc++.a')
    variant('strip',
            default=False,
            description='Strip executables to reduce installation size')

    # https://gcc.gnu.org/install/prerequisites.html
    depends_on('gmp@4.3.2:')
    depends_on('mpfr@2.4.2:')
    depends_on('mpc@0.8.1:', when='@4.5:')
    depends_on('isl@0.14', when='@5:5.9')
    depends_on('isl@0.15:', when='@6:')
    depends_on('zlib', when='@6:')
    depends_on('gnat', when='languages=ada')
    depends_on('binutils~libiberty', when='+binutils')
    depends_on('zip', type='build', when='languages=java')

    # TODO: integrate these libraries.
    # depends_on('ppl')
    # depends_on('cloog')

    # https://gcc.gnu.org/install/test.html
    depends_on('dejagnu@1.4.4', type='test')
    depends_on('expect', type='test')
    depends_on('tcl', type='test')
    depends_on('autogen@5.5.4:', type='test')
    depends_on('guile@1.4.1:', type='test')

    # See https://golang.org/doc/install/gccgo#Releases
    provides('golang',        when='languages=go @4.6:')
    provides('golang@:1',     when='languages=go @4.7.1:')
    provides('golang@:1.1',   when='languages=go @4.8:')
    provides('golang@:1.1.2', when='languages=go @4.8.2:')
    provides('golang@:1.2',   when='languages=go @4.9:')
    provides('golang@:1.4',   when='languages=go @5:')
    provides('golang@:1.6.1', when='languages=go @6:')
    provides('golang@:1.8',   when='languages=go @7:')

    # For a list of valid languages for a specific release,
    # run the following command in the GCC source directory:
    #    $ grep ^language= gcc/*/config-lang.in
    # See https://gcc.gnu.org/install/configure.html

    # Support for processing BRIG 1.0 files was added in GCC 7
    # BRIG is a binary format for HSAIL:
    # (Heterogeneous System Architecture Intermediate Language).
    # See https://gcc.gnu.org/gcc-7/changes.html
    conflicts('languages=brig', when='@:6')

    # BRIG does not seem to be supported on macOS
    conflicts('languages=brig', when='platform=darwin')

    # GCC 4.8 added a 'c' language. I'm sure C was always built,
    # but this is the first version that accepts 'c' as a valid language.
    conflicts('languages=c', when='@:4.7')

    # GCC 4.6 added support for the Go programming language.
    # See https://gcc.gnu.org/gcc-4.6/changes.html
    conflicts('languages=go', when='@:4.5')

    # Go is not supported on macOS
    conflicts('languages=go', when='platform=darwin')

    # The GCC Java frontend and associated libjava runtime library
    # have been removed from GCC as of GCC 7.
    # See https://gcc.gnu.org/gcc-7/changes.html
    conflicts('languages=java', when='@7:')

    # GCC 5 added the ability to build GCC as a Just-In-Time compiler.
    # See https://gcc.gnu.org/gcc-5/changes.html
    conflicts('languages=jit', when='@:4')

    if sys.platform == 'darwin':
        # Fix parallel build on APFS filesystem
        # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=81797
        if macos_version() >= Version('10.13'):
            patch('darwin/apfs.patch', when='@5.5.0,6.1:6.4,7.1:7.3')
            # from homebrew via macports
            # https://trac.macports.org/ticket/56502#no1
            # see also: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=83531
            patch('darwin/headers-10.13-fix.patch', when='@5.5.0')
        patch('darwin/gcc-7.1.0-headerpad.patch', when='@5:')
        patch('darwin/gcc-6.1.0-jit.patch', when='@5:7')
        patch('darwin/gcc-4.9.patch1', when='@4.9.0:4.9.3')
        patch('darwin/gcc-4.9.patch2', when='@4.9.0:4.9.3')

    patch('piclibs.patch', when='+piclibs')
    patch('gcc-backport.patch', when='@4.7:4.9.2,5:5.3')

    # Older versions do not compile with newer versions of glibc
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=81712
    patch('ucontext_t.patch', when='@4.9,5.1:5.4,6.1:6.4,7.1')
    patch('ucontext_t-java.patch', when='@4.9,5.1:5.4,6.1:6.4 languages=java')
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=81066
    patch('stack_t-4.9.patch', when='@4.9')
    patch('stack_t.patch', when='@5.1:5.4,6.1:6.4,7.1')
    # https://bugs.busybox.net/show_bug.cgi?id=10061
    patch('signal.patch', when='@4.9,5.1:5.4')

    build_directory = 'spack-build'

    def url_for_version(self, version):
        url = 'http://ftp.gnu.org/gnu/gcc/gcc-{0}/gcc-{0}.tar.{1}'
        suffix = 'xz'

        if version < Version('6.4.0') or version == Version('7.1.0'):
            suffix = 'bz2'

        if version == Version('5.5.0'):
            suffix = 'xz'

        return url.format(version, suffix)

    def patch(self):
        spec = self.spec
        prefix = self.spec.prefix

        # Fix a standard header file for OS X Yosemite that
        # is GCC incompatible by replacing non-GCC compliant macros
        if 'yosemite' in spec.architecture:
            if os.path.isfile('/usr/include/dispatch/object.h'):
                new_dispatch_dir = join_path(prefix, 'include', 'dispatch')
                mkdirp(new_dispatch_dir)
                new_header = join_path(new_dispatch_dir, 'object.h')
                install('/usr/include/dispatch/object.h', new_header)
                filter_file(r'typedef void \(\^dispatch_block_t\)\(void\)',
                            'typedef void* dispatch_block_t',
                            new_header)

        # Use installed libz
        if self.version >= Version('6'):
            filter_file('@zlibdir@',
                        '-L{0}'.format(spec['zlib'].prefix.lib),
                        'gcc/Makefile.in')
            filter_file('@zlibinc@',
                        '-I{0}'.format(spec['zlib'].prefix.include),
                        'gcc/Makefile.in')

    def configure_args(self):
        spec = self.spec

        # Generic options to compile GCC
        options = [
            '--disable-multilib',
            '--enable-languages={0}'.format(
                ','.join(spec.variants['languages'].value)),
            '--with-mpfr={0}'.format(spec['mpfr'].prefix),
            '--with-gmp={0}'.format(spec['gmp'].prefix),
            '--enable-lto',
            '--with-quad'
        ]

        # Use installed libz
        if self.version >= Version('6'):
            options.append('--with-system-zlib')

        # Enabling language "jit" requires --enable-host-shared.
        if 'languages=jit' in spec:
            options.append('--enable-host-shared')

        # Binutils
        if spec.satisfies('+binutils'):
            static_bootstrap_flags = '-static-libstdc++ -static-libgcc'
            binutils_options = [
                '--with-sysroot=/',
                '--with-stage1-ldflags={0} {1}'.format(
                    self.rpath_args, static_bootstrap_flags),
                '--with-boot-ldflags={0} {1}'.format(
                    self.rpath_args, static_bootstrap_flags),
                '--with-gnu-ld',
                '--with-ld={0}/ld'.format(spec['binutils'].prefix.bin),
                '--with-gnu-as',
                '--with-as={0}/as'.format(spec['binutils'].prefix.bin),
            ]
            options.extend(binutils_options)

        # MPC
        if 'mpc' in spec:
            options.append('--with-mpc={0}'.format(spec['mpc'].prefix))

        # ISL
        if 'isl' in spec:
            options.append('--with-isl={0}'.format(spec['isl'].prefix))

        # macOS
        if sys.platform == 'darwin':
            options.append('--with-build-config=bootstrap-debug')

        return options

    @property
    def build_targets(self):
        if sys.platform == 'darwin':
            return ['bootstrap']
        return []

    @property
    def install_targets(self):
        if '+strip' in self.spec:
            return ['install-strip']
        return ['install']

    @property
    def spec_dir(self):
        # e.g. lib/gcc/x86_64-unknown-linux-gnu/4.9.2
        spec_dir = glob.glob('{0}/gcc/*/*'.format(self.prefix.lib))
        return spec_dir[0] if spec_dir else None

    @run_after('install')
    def write_rpath_specs(self):
        """Generate a spec file so the linker adds a rpath to the libs
           the compiler used to build the executable."""
        if not self.spec_dir:
            tty.warn('Could not install specs for {0}.'.format(
                     self.spec.format('$_$@')))
            return

        gcc = self.spec['gcc'].command
        lines = gcc('-dumpspecs', output=str).strip().split('\n')
        specs_file = join_path(self.spec_dir, 'specs')
        with open(specs_file, 'w') as out:
            for line in lines:
                out.write(line + '\n')
                if line.startswith('*link:'):
                    out.write('-rpath {0}:{1} '.format(
                              self.prefix.lib, self.prefix.lib64))
        set_install_permissions(specs_file)

    def setup_environment(self, spack_env, run_env):
        run_env.set('CC', join_path(self.spec.prefix.bin, 'gcc'))
        run_env.set('CXX', join_path(self.spec.prefix.bin, 'g++'))
        run_env.set('FC', join_path(self.spec.prefix.bin, 'gfortran'))
        run_env.set('F77', join_path(self.spec.prefix.bin, 'gfortran'))
        run_env.set('F90', join_path(self.spec.prefix.bin, 'gfortran'))
