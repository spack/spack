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


class Googletest(CMakePackage):
    """Google test framework for C++.  Also called gtest."""
    homepage = "https://github.com/google/googletest"
    url      = "https://github.com/google/googletest/tarball/release-1.7.0"

    version('1.8.0', 'd2edffbe844902d942c31db70c7cfec2')
    version('1.7.0', '5eaf03ed925a47b37c8e1d559eb19bc4')
    version('1.6.0', '90407321648ab25b067fcd798caf8c78')

    variant('gmock', default=False, description='Build with gmock')
    conflicts('+gmock', when='@:1.7.0')

    variant('pthreads', default=True,
            description='Build multithreaded version with pthreads')
    variant('shared', default=True,
            description='Build shared libraries (DLLs)')

    def cmake_args(self):
        spec = self.spec
        if '@1.8.0:' in spec:
            # New style (contains both Google Mock and Google Test)
            options = ['-DBUILD_GTEST=ON']
            if '+gmock' in spec:
                options.append('-DBUILD_GMOCK=ON')
            else:
                options.append('-DBUILD_GMOCK=OFF')
        else:
            # Old style (contains only GTest)
            options = []

        options.append('-Dgtest_disable_pthreads={0}'.format(
            'ON' if '+pthreads' in spec else 'OFF'))
        options.append('-DBUILD_SHARED_LIBS={0}'.format(
            'ON' if '+shared' in spec else 'OFF'))
        return options

    @when('@:1.7.0')
    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory):
            # Google Test doesn't have a make install
            # We have to do our own install here.
            install_tree(join_path(self.stage.source_path, 'include'),
                         prefix.include)

            mkdirp(prefix.lib)
            if '+shared' in spec:
                install('libgtest.{0}'.format(dso_suffix), prefix.lib)
                install('libgtest_main.{0}'.format(dso_suffix), prefix.lib)
            else:
                install('libgtest.a', prefix.lib)
                install('libgtest_main.a', prefix.lib)
