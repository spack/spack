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


class Googletest(Package):
    """Google test framework for C++.  Also called gtest."""
    homepage = "https://github.com/google/googletest"
    url      = "https://github.com/google/googletest/tarball/release-1.7.0"

    version('1.8.0', 'd2edffbe844902d942c31db70c7cfec2')
    version('1.7.0', '5eaf03ed925a47b37c8e1d559eb19bc4')
    version('1.6.0', '90407321648ab25b067fcd798caf8c78')

    depends_on("cmake", type='build')

    def install(self, spec, prefix):
        which('cmake')('.', *std_cmake_args)

        make()

        # Google Test doesn't have a make install
        # We have to do our own install here.
        install_tree('include', prefix.include)

        mkdirp(prefix.lib)
        install('./libgtest.a', '%s' % prefix.lib)
        install('./libgtest_main.a', '%s' % prefix.lib)
