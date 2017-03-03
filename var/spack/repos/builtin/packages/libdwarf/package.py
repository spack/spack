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

    version('20160507', 'ae32d6f9ece5daf05e2d4b14822ea811')
    version('20130729', '4cc5e48693f7b93b7aa0261e63c0e21d')
    version('20130207', '64b42692e947d5180e162e46c689dfbf')
    version('20130126', 'ded74a5e90edb5a12aac3c29d260c5db')
    depends_on("elf", type='link')

    parallel = False

    def install(self, spec, prefix):

        # elfutils contains a dwarf.h that conflicts with libdwarf's
        # TODO: we should remove this when we can modify the include order
        hide_list = []
        if spec.satisfies('^elfutils'):
            dwarf_h = join_path(spec['elfutils'].prefix, 'include/dwarf.h')
            hide_list.append(dwarf_h)
        with hide_files(*hide_list):
            # dwarf build does not set arguments for ar properly
            make.add_default_arg('ARFLAGS=rcs')

            # Dwarf doesn't provide an install, so we have to do it.
            mkdirp(prefix.bin, prefix.include, prefix.lib, prefix.man1)

            with working_dir('libdwarf'):
                extra_config_args = []

                # this is to prevent picking up system /usr/include/libelf.h
                if spec.satisfies('^libelf'):
                    libelf_inc_dir = join_path(spec['libelf'].prefix,
                                               'include/libelf')
                    extra_config_args.append('CFLAGS=-I{0}'.format(
                                             libelf_inc_dir))
                configure("--prefix=" + prefix, "--enable-shared",
                          *extra_config_args)
                make()

                install('libdwarf.a',  prefix.lib)
                install('libdwarf.so', prefix.lib)
                install('libdwarf.h',  prefix.include)
                install('dwarf.h',     prefix.include)

            if spec.satisfies('@20130126:20130729'):
                dwarfdump_dir = 'dwarfdump2'
            else:
                dwarfdump_dir = 'dwarfdump'
            with working_dir(dwarfdump_dir):
                configure("--prefix=" + prefix)

                # This makefile has strings of copy commands that
                # cause a race in parallel
                make(parallel=False)

                install('dwarfdump',      prefix.bin)
                install('dwarfdump.conf', prefix.lib)
                install('dwarfdump.1',    prefix.man1)
