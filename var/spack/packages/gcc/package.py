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

from contextlib import closing
from glob import glob

class Gcc(Package):
    """The GNU Compiler Collection includes front ends for C, C++,
       Objective-C, Fortran, and Java."""
    homepage = "https://gcc.gnu.org"

    list_url = 'http://open-source-box.org/gcc/'
    list_depth = 2

    version('4.9.2', '4df8ee253b7f3863ad0b86359cd39c43',
            url="http://open-source-box.org/gcc/gcc-4.9.2/gcc-4.9.2.tar.bz2")
    version('4.9.1', 'fddf71348546af523353bd43d34919c1',
            url="http://open-source-box.org/gcc/gcc-4.9.1/gcc-4.9.1.tar.bz2")

    depends_on("mpc")
    depends_on("mpfr")
    depends_on("gmp")
    depends_on("libelf")


    def install(self, spec, prefix):
        # libjava/configure needs a minor fix to install into spack paths.
        filter_file(r"'@.*@'", "'@[[:alnum:]]*@'", 'libjava/configure', string=True)

        # Rest of install is straightforward.
        configure("--prefix=%s" % prefix,
                  "--libdir=%s/lib64" % prefix,
                  "--disable-multilib",
                  "--enable-languages=c,c++,fortran,java,objc,go",
                  "--enable-lto",
                  "--with-quad")
        make()
        make("install")

        self.write_rpath_specs()


    @property
    def spec_dir(self):
        # e.g. lib64/gcc/x86_64-unknown-linux-gnu/4.9.2
        spec_dir = glob("%s/lib64/gcc/*/*" % self.prefix)
        return spec_dir[0] if spec_dir else None


    def write_rpath_specs(self):
        """Generate a spec file so the linker adds a rpath to the libs
           the compiler used to build the executable."""
        if not self.spec_dir:
            tty.warn("Could not install specs for %s." % self.spec.format('$_$@'))
            return

        gcc = Executable(join_path(self.prefix.bin, 'gcc'))
        lines = gcc('-dumpspecs', return_output=True).split("\n")
        for i, line in enumerate(lines):
            if line.startswith("*link:"):
                specs_file = join_path(self.spec_dir, 'specs')
                with closing(open(specs_file, 'w')) as out:
                    out.write(lines[i] + "\n")
                    out.write("-rpath %s/lib:%s/lib64 \\\n"
                                % (self.prefix, self.prefix))
                    out.write(lines[i+1] + "\n")
                set_install_permissions(specs_file)
