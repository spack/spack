# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Guile(AutotoolsPackage):
    """Guile is the GNU Ubiquitous Intelligent Language for Extensions,
    the official extension language for the GNU operating system."""

    homepage = "https://www.gnu.org/software/guile/"
    url      = "https://ftpmirror.gnu.org/guile/guile-2.2.0.tar.gz"

    version('2.2.6', sha256='08c0e7487777740b61cdd97949b69e8a5e2997d8c2fe6c7e175819eb18444506')
    version('2.2.5', sha256='c3c7a2f6ae0d8321a240c7ebc532a1d47af8c63214157a73789e2b2305b4c927')
    version('2.2.4', sha256='33b904c0bf4e48e156f3fb1d0e6b0392033bd610c6c9d9a0410c6e0ea96a3e5c')
    version('2.2.3', sha256='87ee07caef33c97ddc74bf3c29ce7628cfac12061f573e4a29a3a1176754610a')
    version('2.2.2', sha256='3d9b94183b19f04dd4317da87beedafd1c947142f3d861ca1f0224e7a75127ee')
    version('2.2.1', sha256='f004b2a5e98017df80cd419773f12a77cfc7ba6069195f97d6702e3d6e487a14')
    version('2.2.0',  '0d5de8075b965f9ee5ea04399b60a3f9')
    version('2.0.14', '333b6eec83e779935a45c818f712484e')
    version('2.0.11', 'e532c68c6f17822561e3001136635ddd')

    variant('readline', default=True, description='Use the readline library')
    variant('threads', default=True, description='Use the thread interface')

    depends_on('gmp@4.2:')
    depends_on('gettext')
    depends_on('libtool@1.5.6:')
    depends_on('libunistring@0.9.3:')
    depends_on('bdw-gc@7.0:')
    depends_on('libffi')
    depends_on('readline', when='+readline')
    depends_on('pkgconfig', type='build')

    build_directory = 'spack-build'

    conflicts('+threads', when='%intel')

    def configure_args(self):
        spec = self.spec

        config_args = [
            '--with-libunistring-prefix={0}'.format(
                spec['libunistring'].prefix),
            '--with-libltdl-prefix={0}'.format(spec['libtool'].prefix),
            '--with-libgmp-prefix={0}'.format(spec['gmp'].prefix),
            '--with-libintl-prefix={0}'.format(spec['gettext'].prefix),
        ]
        config_args += self.with_or_without('threads')

        if '+readline' in spec:
            config_args.append('--with-libreadline-prefix={0}'.format(
                spec['readline'].prefix))
        else:
            config_args.append('--without-libreadline-prefix')

        return config_args
