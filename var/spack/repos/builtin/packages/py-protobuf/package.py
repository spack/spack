# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyProtobuf(PythonPackage):
    """Protocol buffers are Google's language-neutral, platform-neutral,
    extensible mechanism for serializing structured data - think XML, but
    smaller, faster, and simpler. You define how you want your data to be
    structured once, then you can use special generated source code to easily
    write and read your structured data to and from a variety of data streams
    and using a variety of languages."""

    homepage = 'https://developers.google.com/protocol-buffers/'
    url      = 'https://pypi.io/packages/source/p/protobuf/protobuf-3.0.0b2.tar.gz'

    variant('cpp', default=False,
            description='Enable the cpp implementation')

    version('3.7.1', sha256='21e395d7959551e759d604940a115c51c6347d90a475c9baf471a1a86b5604a9')
    version('3.6.1', sha256='1489b376b0f364bcc6f89519718c057eb191d7ad6f1b395ffd93d1aa45587811')
    version('3.5.2.post1', '3b60685732bd0cbdc802dfcb6071efbcf5d927ce3127c13c33ea1a8efae3aa76')
    version('3.5.2', '09879a295fd7234e523b62066223b128c5a8a88f682e3aff62fb115e4a0d8be0')
    version('3.5.1', '95b78959572de7d7fafa3acb718ed71f482932ddddddbd29ba8319c10639d863')
    version('3.0.0b2', 'f0d3bd2394345a9af4a277cd0302ae83')
    version('2.6.1', '6bf843912193f70073db7f22e2ea55e2')
    version('2.5.0', '338813f3629d59e9579fed9035ecd457')
    version('2.4.1', '72f5141d20ab1bcae6b1e00acfb1068a')
    version('2.3.0', 'bb020c962f252fe81bfda8fb433bafdd')

    depends_on('py-setuptools', type='build')
    depends_on('protobuf', when='+cpp')

    @when('+cpp')
    def build_args(self, spec, prefix):
        return ['--cpp_implementation']

    @when('+cpp')
    def install_args(self, spec, prefix):
        args = super(PyProtobuf, self).install_args(spec, prefix)
        return args + ['--cpp_implementation']

    @run_after('install')
    def fix_import_error(self):
        if str(self.spec['python'].version.up_to(1)) == '2':
            touch = which('touch')
            touch(self.prefix + '/' +
                  self.spec['python'].package.site_packages_dir +
                  '/google/__init__.py')
