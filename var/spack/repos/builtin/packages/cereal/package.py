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
import os
import shutil


class Cereal(Package):
    """cereal is a header-only C++11 serialization library. cereal takes
       arbitrary data types and reversibly turns them into different
       representations, such as compact binary encodings, XML, or
       JSON. cereal was designed to be fast, light-weight, and easy to
       extend - it has no external dependencies and can be easily bundled
       with other code or used standalone.

    """
    homepage = "http://uscilab.github.io/cereal/"
    url      = "https://github.com/USCiLab/cereal/archive/v1.1.2.tar.gz"

    version('1.2.2', '4c56c7b9499dba79404250ef9a040481')
    version('1.2.1', '64476ed74c19068ee543b53ad3992261')
    version('1.2.0', 'e372c9814696481dbdb7d500e1410d2b')
    version('1.1.2', '34d4ad174acbff005c36d4d10e48cbb9')
    version('1.1.1', '0ceff308c38f37d5b5f6df3927451c27')
    version('1.1.0', '9f2d5f72e935c54f4c6d23e954ce699f')
    version('1.0.0', 'd1bacca70a95cec0ddbff68b0871296b')
    version('0.9.1', '8872d4444ff274ce6cd1ed364d0fc0ad')

    patch("Boost.patch")
    patch("Boost2.patch", when="@1.2.2:")
    patch("pointers.patch")

    depends_on('cmake@2.6.2:', type='build')

    def install(self, spec, prefix):
        # Don't use -Werror
        filter_file(r'-Werror', '', 'CMakeLists.txt')

        # configure
        # Boost is only used for self-tests, which we are not running (yet?)
        cmake('.',
              '-DCMAKE_DISABLE_FIND_PACKAGE_Boost=TRUE',
              '-DSKIP_PORTABILITY_TEST=TRUE',
              *std_cmake_args)

        # Build
        make()

        # Install
        shutil.rmtree(join_path(prefix, 'doc'), ignore_errors=True)
        shutil.rmtree(join_path(prefix, 'include'), ignore_errors=True)
        shutil.rmtree(join_path(prefix, 'lib'), ignore_errors=True)
        shutil.copytree('doc', join_path(prefix, 'doc'), symlinks=True)
        shutil.copytree('include', join_path(prefix, 'include'), symlinks=True)
        # Create empty directory to avoid linker warnings later
        os.mkdir(join_path(prefix, 'lib'))
