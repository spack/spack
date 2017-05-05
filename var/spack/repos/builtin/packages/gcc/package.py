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

from contextlib import closing
from glob import glob
import sys
from os.path import isfile


class Gcc(AutotoolsPackage):
    """The GNU Compiler Collection includes front ends for C, C++, Objective-C,
    Fortran, Ada, and Go, as well as libraries for these languages."""

    homepage = 'https://gcc.gnu.org'
    url      = 'http://ftp.gnu.org/gnu/gcc/gcc-7.1.0/gcc-7.1.0.tar.bz2'
    list_url = 'http://ftp.gnu.org/gnu/gcc/'
    list_depth = 1

    version('7.1.0', '6bf56a2bca9dac9dbbf8e8d1036964a8')
    version('6.3.0', '677a7623c7ef6ab99881bc4e048debb6')
    version('6.2.0', '9768625159663b300ae4de2f4745fcc4')
    version('6.1.0', '8fb6cb98b8459f5863328380fbf06bd1')
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

    # Builds all default languages by default.
    # Ada, Go, Jit, and Objective-C++ are not default languages.
    # In that respect, the name 'all' is rather misleading.
    variant('languages',
            default='all',
            values=('all', 'ada', 'brig', 'c', 'c++', 'fortran',
                    'go', 'java', 'jit', 'lto', 'objc', 'obj-c++'),
            multi=True,
            description='Compilers and runtime libraries to build')
    variant('binutils',
            default=sys.platform != 'darwin',
            description='Build via binutils')
    variant('piclibs',
            default=False,
            description='Build PIC versions of libgfortran.a and libstdc++.a')

    # https://gcc.gnu.org/install/prerequisites.html
    depends_on('gmp@4.3.2:')
    depends_on('mpfr@2.4.2:')
    depends_on('mpc@0.8.1:', when='@4.5:')
    depends_on('isl@0.15:', when='@5.0:')
    depends_on('binutils~libiberty', when='+binutils')
    depends_on('zip', type='build')

    # TODO: integrate these libraries.
    # depends_on('gnat', when='languages=ada')
    # depends_on('ppl')
    # depends_on('cloog')

    # TODO: Add a 'test' deptype
    # https://github.com/LLNL/spack/issues/1279
    # depends_on('dejagnu@1.4.4', type='test')
    # depends_on('expect', type='test')
    # depends_on('tcl', type='test')
    # depends_on('autogen@5.5.4:', type='test')
    # depends_on('guile@1.4.1:', type='test')

    if sys.platform == 'darwin':
        patch('darwin/gcc-4.9.patch1', when='@4.9.0:4.9.3')
        patch('darwin/gcc-4.9.patch2', when='@4.9.0:4.9.3')

    # See https://golang.org/doc/install/gccgo#Releases
    provides('golang',        when='languages=go @4.6:')
    provides('golang@:1',     when='languages=go @4.7.1:')
    provides('golang@:1.1',   when='languages=go @4.8:')
    provides('golang@:1.1.2', when='languages=go @4.8.2:')
    provides('golang@:1.2',   when='languages=go @4.9:')
    provides('golang@:1.4',   when='languages=go @5:')
    provides('golang@:1.6.1', when='languages=go @6:')
    provides('golang@:1.8',   when='languages=go @7:')

    patch('piclibs.patch', when='+piclibs')
    patch('gcc-backport.patch', when='@4.7:4.9.2,5:5.3')

    @run_before('autoreconf')
    def check_languages(self):
        """Makes sure all requested languages are valid for a
        specific version of GCC.

        For a list of valid languages for a specific release,
        run the following command in the GCC source directory:

        .. code-block:: console

           $ grep ^language= gcc/*/config-lang.in

        See https://gcc.gnu.org/install/configure.html
        """
        spec = self.spec
        version = self.version

        # Ada is not currently supported as it requires
        # an existing Ada compiler to build.
        if 'languages=ada' in spec:
            raise InstallError('Ada requires GNAT to install')

        # Support for processing BRIG 1.0 files was added in GCC 7
        # BRIG is a binary format for HSAIL:
        # (Heterogeneous System Architecture Intermediate Language).
        # See https://gcc.gnu.org/gcc-7/changes.html
        if version < Version('7') and 'languages=brig' in spec:
            raise InstallError('BRIG is not available before GCC 7')

        # GCC 4.8 added a 'c' language. I'm sure C was always built,
        # but this is the first version that accepts 'c' as a valid language.
        if version < Version('4.8') and 'languages=c' in spec:
            raise InstallError('C is not a valid language before GCC 4.8')

        # GCC 4.6 added support for the Go programming language.
        # See https://gcc.gnu.org/gcc-4.6/changes.html
        if version < Version('4.6') and 'languages=go' in spec:
            raise InstallError('Go is not available before GCC 4.6')

        # The GCC Java frontend and associated libjava runtime library
        # have been removed from GCC as of GCC 7.
        # See https://gcc.gnu.org/gcc-7/changes.html
        if version >= Version('7') and 'languages=java' in spec:
            raise InstallError('Java is no longer available as of GCC 7')

        # GCC 5 added the ability to build GCC as a Just-In-Time compiler.
        # See https://gcc.gnu.org/gcc-5/changes.html
        if version < Version('5') and 'languages=jit' in spec:
            raise InstallError('JIT is not available before GCC 5')

    def configure_args(self):
        spec = self.spec
        prefix = self.spec.prefix

        # Fix a standard header file for OS X Yosemite that
        # is GCC incompatible by replacing non-GCC compliant macros
        if 'yosemite' in spec.architecture:
            if isfile(r'/usr/include/dispatch/object.h'):
                new_dispatch_dir = join_path(prefix, 'include', 'dispatch')
                mkdirp(new_dispatch_dir)
                cp = which('cp')
                new_header = join_path(new_dispatch_dir, 'object.h')
                cp(r'/usr/include/dispatch/object.h', new_header)
                filter_file(r'typedef void \(\^dispatch_block_t\)\(void\)',
                            'typedef void* dispatch_block_t',
                            new_header)

        # Generic options to compile GCC
        options = [
            '--libdir={0}'.format(prefix.lib64),
            '--disable-multilib',
            '--enable-languages={0}'.format(spec.variants['languages'].value),
            '--with-mpfr={0}'.format(spec['mpfr'].prefix),
            '--with-gmp={0}'.format(spec['gmp'].prefix),
            '--enable-lto',
            '--with-quad'
        ]

        # Binutils
        if spec.satisfies('+binutils'):
            static_bootstrap_flags = "-static-libstdc++ -static-libgcc"
            binutils_options = [
                "--with-sysroot=/", "--with-stage1-ldflags=%s %s" %
                (self.rpath_args, static_bootstrap_flags),
                "--with-boot-ldflags=%s %s" %
                (self.rpath_args, static_bootstrap_flags), "--with-gnu-ld",
                "--with-ld=%s/bin/ld" % spec['binutils'].prefix,
                "--with-gnu-as",
                "--with-as=%s/bin/as" % spec['binutils'].prefix
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

    build_directory = 'spack-build'

    @property
    def build_targets(self):
        if sys.platform == 'darwin':
            return ['bootstrap']
        return []

    @property
    def spec_dir(self):
        # e.g. lib64/gcc/x86_64-unknown-linux-gnu/4.9.2
        spec_dir = glob("%s/lib64/gcc/*/*" % self.prefix)
        return spec_dir[0] if spec_dir else None

    @run_after('install')
    def write_rpath_specs(self):
        """Generate a spec file so the linker adds a rpath to the libs
           the compiler used to build the executable."""
        if not self.spec_dir:
            tty.warn("Could not install specs for %s." %
                     self.spec.format('$_$@'))
            return

        gcc = self.spec['gcc'].command
        lines = gcc('-dumpspecs', output=str).strip().split("\n")
        specs_file = join_path(self.spec_dir, 'specs')
        with closing(open(specs_file, 'w')) as out:
            for line in lines:
                out.write(line + "\n")
                if line.startswith("*link:"):
                    out.write("-rpath %s/lib:%s/lib64 \\\n" %
                              (self.prefix, self.prefix))
        set_install_permissions(specs_file)
