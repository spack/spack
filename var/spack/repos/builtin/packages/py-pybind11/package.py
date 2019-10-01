# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
    maintainers = ['ax3l']

    version('develop', branch='master')
    version('2.3.0', sha256='0f34838f2c8024a6765168227ba587b3687729ebf03dc912f88ff75c7aa9cfe8')
    version('2.2.4', 'b69e83658513215b8d1443544d0549b7d231b9f201f6fc787a2b2218b408181e')
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
