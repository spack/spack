# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hermes(CMakePackage):
    """
    Hermes is a heterogeneous-aware, multi-tiered, dynamic, and distributed
    I/O buffering system that aims to significantly accelerate I/O performance.
    """

    homepage = "http://www.cs.iit.edu/~scs/assets/projects/Hermes/Hermes.html"
    git = "https://github.com/HDFGroup/hermes.git"

    maintainers = ['hyoklee']

    version('master', branch='master')
    version('0.4.0-beta', url="https://github.com/HDFGroup/hermes/archive/v0.4.0-be\
ta.tar.gz", sha256='e8bd0b701149844f7f113a55a107e40b3579945d70ca2cb8ce9db5b5a131efd\
b')

    variant('vfd', default=False, description='Enable HDF5 VFD')

    depends_on('mochi-thallium~cereal@0.8.3')
    depends_on('catch2@2.13.3')
    depends_on('or-tools')
    depends_on('mpich@3.3.2:')
    depends_on('hdf5@1.13.0:', when='+vfd')

    def cmake_args(self):
        args = ['-DCMAKE_INSTALL_PREFIX={}'.format(self.prefix),
                '-DHERMES_RPC_THALLIUM=ON',
                '-DHERMES_INSTALL_TESTS=ON',
                '-DBUILD_TESTING=ON']
        if '+vfd' in self.spec:
        if '+vfd' in self.spec:
            args.append(self.define('HERMES_ENABLE_VFD', 'ON'))
        return args

    def set_include(self, env, path):
        env.append_flags('CFLAGS', '-I{}'.format(path))
        env.append_flags('CXXFLAGS', '-I{}'.format(path))

    def set_lib(self, env, path):
        env.prepend_path('LD_LIBRARY_PATH', path)
        env.append_flags('LDFLAGS', '-L{}'.format(path))

    def set_flags(self, env):
        self.set_include(env, '{}/include'.format(self.prefix))
        self.set_include(env, '{}/include'.format(self.prefix))
        self.set_lib(env, '{}/lib'.format(self.prefix))
        self.set_lib(env, '{}/lib64'.format(self.prefix))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        self.set_flags(spack_env)

    def setup_run_environment(self, env):
        self.set_flags(env)
