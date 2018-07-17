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
import os
from spack import *


class Pdt(AutotoolsPackage):
    """Program Database Toolkit (PDT) is a framework for analyzing source
       code written in several programming languages and for making rich
       program knowledge accessible to developers of static and dynamic
       analysis tools. PDT implements a standard program representation,
       the program database (PDB), that can be accessed in a uniform way
       through a class library supporting common PDB operations.

    """
    homepage = "https://www.cs.uoregon.edu/research/pdt/home.php"
    url      = "http://www.cs.uoregon.edu/research/paracomp/pdtoolkit/Download/pdtoolkit-3.22.1.tar.gz"

    version('3.25', '2cad41fcabf4c79cab8780d3b87f7bb4')
    version('3.24', 'b8fa5189e5602276ce225ba497b617e4')
    version('3.23', 'd61e7a631a27b00e58def52950230a2c')
    version('3.22.1', 'b56b9b3e621161c7fd9e4908b944840d')
    version('3.22',   '982d667617802962a1f7fe6c4c31184f')
    version('3.21',   '3092ca0d8833b69992c17e63ae66c263')
    version('3.20',   'c3edabe202926abe04552e33cd39672d')
    version('3.19',   '5c5e1e6607086aa13bf4b1b9befc5864')
    version('3.18.1', 'e401534f5c476c3e77f05b7f73b6c4f2')

    def patch(self):
        if self.spec.satisfies('%clang'):
            filter_file(r'PDT_GXX=g\+\+ ',
                        r'PDT_GXX=clang++ ', 'ductape/Makefile')

    def configure(self, spec, prefix):
        options = ['-prefix=%s' % prefix]
        if self.compiler.name == 'xl':
            options.append('-XLC')
        elif self.compiler.name == 'intel':
            options.append('-icpc')
        elif self.compiler.name == 'pgi':
            options.append('-pgCC')

        configure(*options)

    @run_after('install')
    def link_arch_dirs(self):
        # Link arch-specific directories into prefix
        for dir in os.listdir(self.prefix):
            path = join_path(self.prefix, dir)
            if not os.path.isdir(path) or os.path.islink(path):
                continue
            for d in ('bin', 'lib'):
                src = join_path(path, d)
                dst = join_path(self.prefix, d)
                if os.path.isdir(src) and not os.path.exists(dst):
                    os.symlink(join_path(dir, d), dst)
