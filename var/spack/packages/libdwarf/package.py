##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
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
    url      = "http://www.prevanders.net/libdwarf-20130729.tar.gz"
    list_url = homepage

    version('20130729', '4cc5e48693f7b93b7aa0261e63c0e21d')
    version('20130207', '64b42692e947d5180e162e46c689dfbf')
    version('20130126', 'ded74a5e90edb5a12aac3c29d260c5db')

    depends_on("libelf")

    parallel = False


    def install(self, spec, prefix):
        # dwarf build does not set arguments for ar properly
        make.add_default_arg('ARFLAGS=rcs')

        # Dwarf doesn't provide an install, so we have to do it.
        mkdirp(prefix.bin, prefix.include, prefix.lib, prefix.man1)

        with working_dir('libdwarf'):
            configure("--prefix=" + prefix, "--enable-shared")
            make()

            install('libdwarf.a',  prefix.lib)
            install('libdwarf.so', prefix.lib)
            install('libdwarf.h',  prefix.include)
            install('dwarf.h',     prefix.include)

        with working_dir('dwarfdump2'):
            configure("--prefix=" + prefix)

            # This makefile has strings of copy commands that
            # cause a race in parallel
            make(parallel=False)

            install('dwarfdump',      prefix.bin)
            install('dwarfdump.conf', prefix.lib)
            install('dwarfdump.1',    prefix.man1)
