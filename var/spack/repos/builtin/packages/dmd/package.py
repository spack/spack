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


class Dmd(MakefilePackage):
    """DMD is the reference compiler for the D programming language."""

    homepage = "https://github.com/dlang/dmd"
    url      = "https://github.com/dlang/dmd/archive/v2.081.1.tar.gz"

    version('2.081.1', sha256='14f3aafe1c93c86646aaeb3ed7361a5fc5a24374cf25c8848c81942bfd9fae1a')

    depends_on('openssl')
    depends_on('curl')

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix.linux.bin64)

    def edit(self, spec, prefix):
        makefile = FileFilter('posix.mak')
        makefile.filter('$(PWD)/../install', prefix, string=True)

    def build(self, spec, prefix):
        make('-f', 'posix.mak', 'AUTO_BOOTSTRAP=1')

    def install(self, spec, prefix):
        make('-f', 'posix.mak', 'install', 'AUTO_BOOTSTRAP=1')
        install_tree('src', prefix.src)
