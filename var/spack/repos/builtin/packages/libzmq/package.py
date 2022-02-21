# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys


class Libzmq(AutotoolsPackage):
    """The ZMQ networking/concurrency library and core API"""

    homepage = "https://zguide.zeromq.org/"
    url      = "https://github.com/zeromq/libzmq/releases/download/v4.3.2/zeromq-4.3.2.tar.gz"
    git      = "https://github.com/zeromq/libzmq.git"

    version('master', branch='master')
    version('4.3.4', sha256='c593001a89f5a85dd2ddf564805deb860e02471171b3f204944857336295c3e5')
    version('4.3.3', sha256='9d9285db37ae942ed0780c016da87060497877af45094ff9e1a1ca736e3875a2')
    version('4.3.2', sha256='ebd7b5c830d6428956b67a0454a7f8cbed1de74b3b01e5c33c5378e22740f763')
    version('4.3.1', sha256='bcbabe1e2c7d0eec4ed612e10b94b112dd5f06fcefa994a0c79a45d835cd21eb')
    version('4.3.0', sha256='8e9c3af6dc5a8540b356697081303be392ade3f014615028b3c896d0148397fd')
    version('4.2.5', sha256='cc9090ba35713d59bb2f7d7965f877036c49c5558ea0c290b0dcc6f2a17e489f')
    version('4.2.2', sha256='5b23f4ca9ef545d5bd3af55d305765e3ee06b986263b31967435d285a3e6df6b')
    version('4.1.4', sha256='e99f44fde25c2e4cb84ce440f87ca7d3fe3271c2b8cfbc67d55e4de25e6fe378')
    version('4.1.2', sha256='f9162ead6d68521e5154d871bac304f88857308bb02366b81bb588497a345927')
    version('4.1.1', sha256='43d61e5706b43946aad4a661400627bcde9c63cc25816d4749c67b64c3dab8db')
    version('4.0.7', sha256='e00b2967e074990d0538361cc79084a0a92892df2c6e7585da34e4c61ee47b03')
    version('4.0.6', sha256='28a2a9c9b77014c39087a498942449df18bb9885cdb63334833525a1d19f2894')
    version('4.0.5', sha256='3bc93c5f67370341428364ce007d448f4bb58a0eaabd0a60697d8086bc43342b')

    variant("libsodium", default=True,
            description="Build with message encryption support via libsodium")

    variant("drafts", default=False,
            description="Build and install draft classes and methods")

    variant("docs", default=True,
            description="Build documentation")

    variant("libbsd", when='@4.3.3:', default=(sys.platform != 'darwin'),
            description="Use strlcpy from libbsd " +
                        "(will use own implementation if false)")

    depends_on("libsodium", when='+libsodium')
    depends_on("libsodium@:1.0.3", when='+libsodium@:4.1.2')

    depends_on('autoconf', type='build', when='@develop')
    depends_on('automake', type='build', when='@develop')
    depends_on('libtool', type='build', when='@develop')
    depends_on('pkgconfig', type='build')
    depends_on('docbook-xml', type='build', when='+docs')
    depends_on('docbook-xsl', type='build', when='+docs')

    depends_on('libbsd', when='+libbsd')

    conflicts('%gcc@8:', when='@:4.2.2')

    # Fix aggressive compiler warning false positive
    patch('https://github.com/zeromq/libzmq/commit/92b2c38a2c51a1942a380c7ee08147f7b1ca6845.patch', sha256='8ebde83ee148989f9118d36ebaf256532627b8a6e7a486842110623331972edb', when='@4.2.3:4.3.4 %gcc@11:')

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

        config_args.extend(self.enable_or_disable("drafts"))
        config_args.extend(self.enable_or_disable("libbsd"))

        if '+libsodium' in self.spec:
            config_args.append('--with-libsodium')
        if '~docs' in self.spec:
            config_args.append('--without-docs')
        if 'clang' in self.compiler.cc:
            config_args.append("CFLAGS=-Wno-gnu")
            config_args.append("CXXFLAGS=-Wno-gnu")
        return config_args
