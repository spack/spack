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
    url      = 'https://pypi.io/packages/source/p/protobuf/protobuf-3.7.1.tar.gz'

    variant('cpp', default=False,
            description='Enable the cpp implementation')

    version('3.7.1', sha256='21e395d7959551e759d604940a115c51c6347d90a475c9baf471a1a86b5604a9')
    version('3.6.1', sha256='1489b376b0f364bcc6f89519718c057eb191d7ad6f1b395ffd93d1aa45587811')
    version('3.6.0', sha256='a37836aa47d1b81c2db1a6b7a5e79926062b5d76bd962115a0e615551be2b48d')
    version('3.5.2', sha256='09879a295fd7234e523b62066223b128c5a8a88f682e3aff62fb115e4a0d8be0')
    version('3.5.1', sha256='95b78959572de7d7fafa3acb718ed71f482932ddddddbd29ba8319c10639d863')
    version('3.4.0', sha256='ef02609ef445987976a3a26bff77119c518e0915c96661c3a3b17856d0ef6374')
    version('3.3.0', sha256='1cbcee2c45773f57cb6de7ee0eceb97f92b9b69c0178305509b162c0160c1f04')
    version('2.6.1', sha256='8faca1fb462ee1be58d00f5efb4ca4f64bde92187fe61fde32615bbee7b3e745')
    version('2.5.0', sha256='58292c459598c9297258bf57acc055f701c727f0154a86af8c0947dde37d8172')
    version('2.4.1', sha256='df30b98acb6ef892da8b4776175510cff2131908fd0526b6bad960c55a830a1b')
    version('2.3.0', sha256='374bb047874a506507912c3717d0ce62affbaa9a22bcb494d63d60326a0867b5')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-six@1.9:', when='@3:', type=('build', 'run'))
    depends_on('py-ordereddict', when='@3: ^python@:2', type=('build', 'run'))
    depends_on('py-unittest2', when='@3: ^python@:2', type=('build', 'run'))
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
