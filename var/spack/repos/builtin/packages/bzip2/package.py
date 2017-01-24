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


class Bzip2(Package):
    """bzip2 is a freely available, patent free high-quality data
    compressor. It typically compresses files to within 10% to 15%
    of the best available techniques (the PPM family of statistical
    compressors), whilst being around twice as fast at compression
    and six times faster at decompression."""

    homepage = "http://www.bzip.org"
    url      = "http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz"

    version('1.0.6', '00b516f4704d4a7cb50a1d97e6e8e15b')
    variant('shared', default=True, description='Enables the build of shared libraries.')

    def patch(self):
        # bzip2 comes with two separate Makefiles for static and dynamic builds
        # Tell both to use Spack's compiler wrapper instead of GCC
        filter_file(r'^CC=gcc', 'CC=cc', 'Makefile')
        filter_file(r'^CC=gcc', 'CC=cc', 'Makefile-libbz2_so')

        # Patch the link line to use RPATHs on macOS
        if 'darwin' in self.spec.architecture:
            v = self.spec.version
            v1, v2, v3 = (v.up_to(i) for i in (1, 2, 3))

            kwargs = {'ignore_absent': False, 'backup': False, 'string': True}

            mf = FileFilter('Makefile-libbz2_so')
            mf.filter('$(CC) -shared -Wl,-soname -Wl,libbz2.so.{0} -o libbz2.so.{1} $(OBJS)'  # noqa
                      .format(v2, v3),
                      '$(CC) -dynamiclib -Wl,-install_name -Wl,@rpath/libbz2.{0}.dylib -current_version {1} -compatibility_version {2} -o libbz2.{3}.dylib $(OBJS)'  # noqa
                      .format(v1, v2, v3, v3),
                      **kwargs)

            mf.filter(
                '$(CC) $(CFLAGS) -o bzip2-shared bzip2.c libbz2.so.{0}'.format(v3),  # noqa
                '$(CC) $(CFLAGS) -o bzip2-shared bzip2.c libbz2.{0}.dylib'
                .format(v3), **kwargs)
            mf.filter(
                'rm -f libbz2.so.{0}'.format(v2),
                'rm -f libbz2.{0}.dylib'.format(v2), **kwargs)
            mf.filter(
                'ln -s libbz2.so.{0} libbz2.so.{1}'.format(v3, v2),
                'ln -s libbz2.{0}.dylib libbz2.{1}.dylib'.format(v3, v2),
                **kwargs)

    def install(self, spec, prefix):
        # Build the dynamic library first
        if '+shared' in spec:
            make('-f', 'Makefile-libbz2_so')

        # Build the static library and everything else
        make()
        make('install', 'PREFIX={0}'.format(prefix))

        if '+shared' in spec:
            install('bzip2-shared', join_path(prefix.bin, 'bzip2'))

            v1, v2, v3 = (self.spec.version.up_to(i) for i in (1, 2, 3))
            if 'darwin' in self.spec.architecture:
                lib = 'libbz2.dylib'
                lib1, lib2, lib3 = ('libbz2.{0}.dylib'.format(v)
                                    for v in (v1, v2, v3))
            else:
                lib = 'libbz2.so'
                lib1, lib2, lib3 = ('libbz2.so.{0}'.format(v)
                                    for v in (v1, v2, v3))

            install(lib3, join_path(prefix.lib, lib3))
            with working_dir(prefix.lib):
                for l in (lib, lib1, lib2):
                    symlink(lib3, l)

        with working_dir(prefix.bin):
            force_remove('bunzip2', 'bzcat')
            symlink('bzip2', 'bunzip2')
            symlink('bzip2', 'bzcat')
