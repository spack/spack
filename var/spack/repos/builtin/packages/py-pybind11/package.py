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


class PyPybind11(CMakePackage):
    """pybind11 -- Seamless operability between C++11 and Python.
    pybind11 is a lightweight header-only library that exposes C++ types in
    Python and vice versa, mainly to create Python bindings of existing C++
    code. Its goals and syntax are similar to the excellent Boost.Python
    library by David Abrahams: to minimize boilerplate code in traditional
    extension modules by inferring type information using compile-time
    introspection."""

    homepage = "https://pybind11.readthedocs.io"
    url      = "https://github.com/pybind/pybind11/archive/v2.1.0.tar.gz"
    git      = "https://github.com/pybind/pybind11.git"

    version('develop', branch='master')
    version('2.2.3', '55b637945bbf47d99d2c906bf0c13f49')
    version('2.2.2', 'fc174e1bbfe7ec069af7eea86ec37b5c')
    version('2.2.1', 'bab1d46bbc465af5af3a4129b12bfa3b')
    version('2.2.0', '978b26aea1c6bfc4f88518ef33771af2')
    version('2.1.1', '5518988698df937ccee53fb6ba91d12a')
    version('2.1.0', '3cf07043d677d200720c928569635e12')

    depends_on('py-pytest', type='test')
    depends_on('py-setuptools', type='build')

    extends('python')

    # compiler support
    conflicts('%gcc@:4.7')
    conflicts('%clang@:3.2')
    conflicts('%intel@:16')

    def cmake_args(self):
        args = []
        args.append('-DPYTHON_EXECUTABLE:FILEPATH=%s'
                    % self.spec['python'].command.path)
        args += [
            '-DPYBIND11_TEST:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF')
        ]
        return args

    def setup_environment(self, spack_env, run_env):
        spack_env.set('PYBIND11_USE_CMAKE', 1)

    def install(self, spec, prefix):
        super(PyPybind11, self).install(spec, prefix)
        setup_py('install', '--single-version-externally-managed', '--root=/',
                 '--prefix={0}'.format(prefix))
