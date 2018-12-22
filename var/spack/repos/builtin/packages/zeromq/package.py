# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Zeromq(AutotoolsPackage):
    """The ZMQ networking/concurrency library and core API"""

    homepage = "http://zguide.zeromq.org/"
    url      = "http://download.zeromq.org/zeromq-4.1.2.tar.gz"
    git      = "https://github.com/zeromq/libzmq.git"

    version('develop', branch='master')
    version('4.2.5', 'a1c95b34384257e986842f4d006957b8',
            url='https://github.com/zeromq/libzmq/releases/download/v4.2.5/zeromq-4.2.5.tar.gz')
    version('4.2.2', '52499909b29604c1e47a86f1cb6a9115')
    version('4.1.4', 'a611ecc93fffeb6d058c0e6edf4ad4fb')
    version('4.1.2', '159c0c56a895472f02668e692d122685')
    version('4.1.1', '0a4b44aa085644f25c177f79dc13f253')
    version('4.0.7', '9b46f7e7b0704b83638ef0d461fd59ab')
    version('4.0.6', 'd47dd09ed7ae6e7fd6f9a816d7f5fdf6')
    version('4.0.5', '73c39f5eb01b9d7eaf74a5d899f1d03d')

    variant("libsodium", default=True, description="Build with libsodium support")

    depends_on("libsodium", when='+libsodium')
    depends_on("libsodium@:1.0.3", when='+libsodium@:4.1.2')

    depends_on('autoconf', type='build', when='@develop')
    depends_on('automake', type='build', when='@develop')
    depends_on('libtool', type='build', when='@develop')
    depends_on('pkgconfig', type='build')

    conflicts('%gcc@8:', when='@:4.2.2')

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
