##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import os
import inspect


class YamlCpp(CMakePackage):
    """A YAML parser and emitter in C++"""

    homepage = "https://github.com/jbeder/yaml-cpp"
    url      = "https://github.com/jbeder/yaml-cpp/archive/yaml-cpp-0.5.3.tar.gz"

    version('0.5.3', '2bba14e6a7f12c7272f87d044e4a7211')
    version('develop', git='https://github.com/jbeder/yaml-cpp', branch='master')

    variant('shared', default=True,
            description='Additionally build shared libraries')
    variant('pic',   default=True,
            description='Build with position independent code')

    depends_on('boost', when='@:0.5.3')

    def cmake_args(self):
        options = []

        options.extend([
            '-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=%s' % (
                'ON' if '+pic' in self.spec else 'OFF'),
        ])

        return options

    def cmake(self, spec, prefix):
        options = [os.path.abspath(self.root_cmakelists_dir)]
        options += self.std_cmake_args
        options += self.cmake_args()
        with working_dir(self.build_directory, create=True):
            inspect.getmodule(self).cmake(*options)
            inspect.getmodule(self).make(*self.build_targets)
            inspect.getmodule(self).make(*self.install_targets)
        if '+shared' in self.spec:
            options += ['-DBUILD_SHARED_LIBS:BOOL=ON']
            with working_dir(self.build_directory, create=True):
                inspect.getmodule(self).cmake(*options)
                inspect.getmodule(self).make(*self.build_targets)
                inspect.getmodule(self).make(*self.install_targets)

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        pass
