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


class Oclint(Package):
    """OClint: a static analysis tool for C, C++, and Objective-C code

       OCLint is a static code analysis tool for improving quality and
       reducing defects by inspecting C, C++ and Objective-C code and
       looking for potential problems"""

    homepage = "http://oclint.org/"
    url      = "https://github.com/oclint/oclint/archive/v0.13.tar.gz"

    version('0.13', '1d0e605eb7815ac15e6a2a82327d2dd8')

    depends_on('python', type=('build'))
    depends_on('py-argparse', type=('build'))
    depends_on('git', type=('build'))
    depends_on('subversion', type=('build'))
    depends_on('cmake', type=('build'))
    depends_on('ninja', type=('build'))
    depends_on('llvm@5.0.0:')

    # Needed to fix a bug in oclint-scripts/bundle script, which
    # attempts to install c++ headers in the wrong location
    # contributed upstream as
    # https://github.com/oclint/oclint/pull/492
    patch('bundle.patch', level=0)

    def install(self, spec, prefix):
        # Build from source via directions from
        # http://docs.oclint.org/en/stable/intro/build.html,
        cd('oclint-scripts')

        # ...but instead of using oclint-scripts/make, execute the
        # commands in oclint-scripts/makeWithSystemLLVM so that
        # oclint links to spack-installed LLVM
        build_script = Executable(join_path('.', 'build'))
        bundle_script = Executable(join_path('.', 'bundle'))

        # Add the '-no-analytics' argument to the build script because
        # 1) it doesn't detect properly a spack install of OpenSSL,
        #    and throws an error due to missing OpenSSL headers
        # 2) the bespoke build system is a pain to patch as it is
        # 3) many sites don't allow software that communicates analytics data
        build_script('-release',
                     '-clean',
                     '-llvm-root={0}'.format(spec['llvm'].prefix),
                     '-use-system-compiler',
                     '-no-analytics',
                     'all')
        bundle_script('-release', '-llvm-root={0}'.format(spec['llvm'].prefix))

        # Copy install tree into the correct locations using the
        # directory layout described in
        cd(join_path('..', 'build'))
        install_tree(join_path('oclint-release', 'include'), prefix.include)
        install_tree(join_path('oclint-release', 'lib'), prefix.lib)
        install_tree(join_path('oclint-release', 'bin'), prefix.bin)
