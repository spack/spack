# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyGrpcioTools(PythonPackage):
    """Protobuf code generator for gRPC"""

    homepage = "https://grpc.io/"
    pypi     = "grpcio-tools/grpcio-tools-1.42.0.tar.gz"

    version('1.42.0', sha256='d0a0daa82eb2c2fb8e12b82a458d1b7c5516fe1135551da92b1a02e2cba93422')
    version('1.39.0', sha256='39dfe7415bc0d3860fdb8dd90607594b046b88b57dbe64284efa4820f951c805')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-protobuf@3.5.0.post1:3', type=('build', 'run'))
    depends_on('py-grpcio@1.42.0:', type=('build', 'run'), when='@1.42.0:')
    depends_on('py-grpcio@1.39.0:', type=('build', 'run'), when='@1.39.0:1.41')
    depends_on('py-cython@0.23:', type='build')
    depends_on('openssl')
    depends_on('zlib')
    depends_on('c-ares')
    depends_on('re2+shared')

    def setup_build_environment(self, env):
        env.set('GRPC_PYTHON_BUILD_WITH_CYTHON', True)
        env.set('GRPC_PYTHON_BUILD_SYSTEM_OPENSSL', True)
        env.set('GRPC_PYTHON_BUILD_SYSTEM_ZLIB', True)
        env.set('GRPC_PYTHON_BUILD_SYSTEM_CARES', True)
        env.set('GRPC_PYTHON_BUILD_SYSTEM_RE2', True)
        # https://github.com/grpc/grpc/pull/24449
        env.set('GRPC_BUILD_WITH_BORING_SSL_ASM', '')
        env.set('GRPC_PYTHON_BUILD_EXT_COMPILER_JOBS', str(make_jobs))

        for dep in self.spec.dependencies(deptype='link'):
            query = self.spec[dep.name]
            env.prepend_path('LIBRARY_PATH', query.libs.directories[0])
            env.prepend_path('CPATH', query.headers.directories[0])

    def patch(self):
        if self.spec.satisfies('%fj'):
            filter_file("-std=gnu99", "", "setup.py")

        # use the spack packages
        filter_file(r'(\s+SSL_INCLUDE = ).*',
                    r"\1('{0}',)".format(self.spec['openssl'].prefix.include),
                    'setup.py')
        filter_file(r'(\s+ZLIB_INCLUDE = ).*',
                    r"\1('{0}',)".format(self.spec['zlib'].prefix.include),
                    'setup.py')
        filter_file(r'(\s+CARES_INCLUDE = ).*',
                    r"\1('{0}',)".format(self.spec['c-ares'].prefix.include),
                    'setup.py')
        filter_file(r'(\s+RE2_INCLUDE = ).*',
                    r"\1('{0}',)".format(self.spec['re2'].prefix.include),
                    'setup.py')
