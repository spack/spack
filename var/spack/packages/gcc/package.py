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

    url = "http://open-source-box.org/gcc/gcc-4.9.2/gcc-4.9.2.tar.bz2"
    list_url = 'http://open-source-box.org/gcc/'
    list_depth = 2

    version('4.9.2', '4df8ee253b7f3863ad0b86359cd39c43')
    version('4.9.1', 'fddf71348546af523353bd43d34919c1')
    version('4.8.4', '5a84a30839b2aca22a2d723de2a626ec')
    version('4.7.4', '4c696da46297de6ae77a82797d2abe28')
    version('4.6.4', 'b407a3d1480c11667f293bfb1f17d1a4')
    version('4.5.4', '27e459c2566b8209ab064570e1b378f7')

    depends_on("mpfr")
    depends_on("gmp")
    depends_on("mpc")     # when @4.5:
    depends_on("libelf")
    depends_on("binutils")

    # Save these until we can do optional deps.
    #depends_on("isl")
    #depends_on("ppl")
    #depends_on("cloog")

    def install(self, spec, prefix):
        # libjava/configure needs a minor fix to install into spack paths.
        filter_file(r"'@.*@'", "'@[[:alnum:]]*@'", 'libjava/configure', string=True)

        enabled_languages = set(('c', 'c++', 'fortran', 'java', 'objc'))
        if spec.satisfies("@4.7.1:"):
            enabled_languages.add('go')

        # Rest of install is straightforward.
        configure("--prefix=%s" % prefix,
                  "--libdir=%s/lib64" % prefix,
                  "--disable-multilib",
                  "--enable-languages=" + ','.join(enabled_languages),
                  "--with-mpc=%s"    % spec['mpc'].prefix,
                  "--with-mpfr=%s"   % spec['mpfr'].prefix,
                  "--with-gmp=%s"    % spec['gmp'].prefix,
                  "--with-libelf=%s" % spec['libelf'].prefix,
                  "--with-stage1-ldflags=%s" % self.rpath_args,
                  "--with-boot-ldflags=%s"   % self.rpath_args,
                  "--enable-lto",
                  "--with-gnu-ld",
                  "--with-ld=%s/bin/ld" % spec['binutils'].prefix,
                  "--with-gnu-as",
                  "--with-as=%s/bin/as" % spec['binutils'].prefix,
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
