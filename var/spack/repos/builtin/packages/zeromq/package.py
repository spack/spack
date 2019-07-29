# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Zeromq(AutotoolsPackage):
    """The ZMQ networking/concurrency library and core API"""

    homepage = "http://zguide.zeromq.org/"
    url      = "https://github.com/zeromq/libzmq/releases/download/v4.3.2/zeromq-4.3.2.tar.gz"
    git      = "https://github.com/zeromq/libzmq.git"

    version('develop', branch='master')
    version('4.3.2', sha256='ebd7b5c830d6428956b67a0454a7f8cbed1de74b3b01e5c33c5378e22740f763')
    version('4.3.1', sha256='bcbabe1e2c7d0eec4ed612e10b94b112dd5f06fcefa994a0c79a45d835cd21eb')
    version('4.3.0', sha256='8e9c3af6dc5a8540b356697081303be392ade3f014615028b3c896d0148397fd')
    version('4.2.5', 'a1c95b34384257e986842f4d006957b8')
    version('4.2.2', '52499909b29604c1e47a86f1cb6a9115')
    version('4.1.4', 'a611ecc93fffeb6d058c0e6edf4ad4fb')
    version('4.1.2', '159c0c56a895472f02668e692d122685')
    version('4.1.1', '0a4b44aa085644f25c177f79dc13f253')
    version('4.0.7', '9b46f7e7b0704b83638ef0d461fd59ab')
    version('4.0.6', 'd47dd09ed7ae6e7fd6f9a816d7f5fdf6')
    version('4.0.5', '73c39f5eb01b9d7eaf74a5d899f1d03d')

    variant("libsodium", default=True,
            description="Build with message encryption support via libsodium")

    depends_on("libsodium", when='+libsodium')
    depends_on("libsodium@:1.0.3", when='+libsodium@:4.1.2')

    depends_on('autoconf', type='build', when='@develop')
    depends_on('automake', type='build', when='@develop')
    depends_on('libtool', type='build', when='@develop')
    depends_on('pkgconfig', type='build')

    conflicts('%gcc@8:', when='@:4.2.2')

    def url_for_version(self, version):
        if version <= Version('4.1.4'):
            url = "http://download.zeromq.org/zeromq-{0}.tar.gz"
        else:
            url = "https://github.com/zeromq/libzmq/releases/download/v{0}/zeromq-{0}.tar.gz"
        return url.format(version)

    @when('@develop')
    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')

    def configure_args(self):
        config_args = []
        if '+libsodium' in self.spec:
            config_args.append('--with-libsodium')
        if 'clang' in self.compiler.cc:
            config_args.append("CFLAGS=-Wno-gnu")
            config_args.append("CXXFLAGS=-Wno-gnu")
        return config_args
