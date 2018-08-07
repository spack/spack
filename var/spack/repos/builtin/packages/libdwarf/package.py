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
import sys
import os

# Only build certain parts of dwarf because the other ones break.
dwarf_dirs = ['libdwarf', 'dwarfdump2']


class Libdwarf(Package):
    """The DWARF Debugging Information Format is of interest to
       programmers working on compilers and debuggers (and any one
       interested in reading or writing DWARF information). It was
       developed by a committee (known as the PLSIG at the time)
       starting around 1991. Starting around 1991 SGI developed the
       libdwarf and dwarfdump tools for internal use and as part of
       SGI IRIX developer tools. Since that time dwarfdump and
       libdwarf have been shipped (as an executable and archive
       respectively, not source) with every release of the SGI
       MIPS/IRIX C compiler."""

    homepage = "http://www.prevanders.net/dwarf.html"
    url      = "http://www.prevanders.net/libdwarf-20160507.tar.gz"
    list_url = homepage

    version('20180129', 'c5e90fad4640f0d713ae8b986031f959')
    version('20160507', 'ae32d6f9ece5daf05e2d4b14822ea811')
    version('20130729', '4cc5e48693f7b93b7aa0261e63c0e21d')
    version('20130207', '64b42692e947d5180e162e46c689dfbf')
    version('20130126', 'ded74a5e90edb5a12aac3c29d260c5db')
    depends_on("elfutils@0.163", when='@20160507', type='link')
    depends_on("elf", type='link')
    depends_on('zlib', type='link')

    parallel = False

    def patch(self):
        filter_file(r'^typedef struct Elf Elf;$', '', 'libdwarf/libdwarf.h.in')

    def install(self, spec, prefix):
        # dwarf build does not set arguments for ar properly
        make.add_default_arg('ARFLAGS=rcs')

        # Dwarf doesn't provide an install, so we have to do it.
        mkdirp(prefix.bin, prefix.include, prefix.lib, prefix.man.man1)

        with working_dir('libdwarf'):
            extra_config_args = []

            # this is to prevent picking up system /usr/include/libelf.h
            if spec.satisfies('^libelf'):
                libelf_inc_dir = join_path(spec['libelf'].prefix,
                                           'include/libelf')
                extra_config_args.append(
                    'CFLAGS=-I{0} -Wl,-L{1} -Wl,-lelf'.format(
                        libelf_inc_dir, spec['libelf'].prefix.lib))
            configure("--prefix=" + prefix, "--enable-shared",
                      *extra_config_args)
            filter_file(r'^dwfzlib\s*=\s*-lz',
                        'dwfzlib=-L{0} -lz'.format(
                            self.spec['zlib'].prefix.lib),
                        'Makefile')
            make()

            libdwarf_name = 'libdwarf.{0}'.format(dso_suffix)
            libdwarf1_name = 'libdwarf.{0}'.format(dso_suffix) + ".1"
            install('libdwarf.a',  prefix.lib)
            install('libdwarf.so', join_path(prefix.lib, libdwarf1_name))
            if spec.satisfies('@20160507:'):
                with working_dir(prefix.lib):
                    os.symlink(libdwarf1_name, libdwarf_name)
            install('libdwarf.h',  prefix.include)
            install('dwarf.h',     prefix.include)

            # It seems like fix_darwin_install_name can't be used
            # here directly; the install name of the library in
            # the stage directory must be fixed in order for dyld
            # to locate it on Darwin when spack builds dwarfdump
            if sys.platform == 'darwin':
                install_name_tool = which('install_name_tool')
                install_name_tool('-id',
                                  join_path('..', 'libdwarf',
                                            'libdwarf.so'),
                                  'libdwarf.so')

        if spec.satisfies('@20130126:20130729'):
            dwarfdump_dir = 'dwarfdump2'
        else:
            dwarfdump_dir = 'dwarfdump'
        with working_dir(dwarfdump_dir):
            configure("--prefix=" + prefix)
            filter_file(r'^dwfzlib\s*=\s*-lz',
                        'dwfzlib=-L{0} -lz'.format(
                            self.spec['zlib'].prefix.lib),
                        'Makefile')

            # This makefile has strings of copy commands that
            # cause a race in parallel
            make(parallel=False)

            install('dwarfdump',      prefix.bin)
            install('dwarfdump.conf', prefix.lib)
            install('dwarfdump.1',    prefix.man.man1)

    @run_after('install')
    def darwin_fix(self):
        if sys.platform == 'darwin':
            fix_darwin_install_name(self.prefix.lib)
