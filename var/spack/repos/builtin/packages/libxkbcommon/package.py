# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxkbcommon(MesonPackage):
    """xkbcommon is a library to handle keyboard descriptions, including
    loading them from disk, parsing them and handling their state. It's mainly
    meant for client toolkits, window systems, and other system
    applications."""

    homepage = "https://xkbcommon.org/"
    url      = "https://xkbcommon.org/download/libxkbcommon-0.8.2.tar.xz"

    version('1.4.0', sha256='106cec5263f9100a7e79b5f7220f889bc78e7d7ffc55d2b6fdb1efefb8024031')
    version('0.8.2', sha256='7ab8c4b3403d89d01898066b72cb6069bddeb5af94905a65368f671a026ed58c', deprecated=True)
    version('0.8.0', sha256='e829265db04e0aebfb0591b6dc3377b64599558167846c3f5ee5c5e53641fe6d', deprecated=True)
    version('0.7.1', sha256='ba59305d2e19e47c27ea065c2e0df96ebac6a3c6e97e28ae5620073b6084e68b', deprecated=True)

    variant('wayland', default=False, description='Enable Wayland support')

    depends_on('pkgconfig@0.9.0:', type='build')
    depends_on('bison', type='build')
    depends_on('util-macros')
    depends_on('xkbdata')
    depends_on('libxcb@1.10:')
    depends_on('libxml2', when='@1:')

    depends_on('wayland@1.2.0:', when='+wayland')
    depends_on('wayland-protocols@1.7:', when='+wayland')

    def meson_args(self):
        return [
            '-Dxkb-config-root={0}'.format(self.spec['xkbdata'].prefix),
            '-Denable-docs=false',
            '-Denable-wayland=' + str(self.spec.satisfies('+wayland'))
        ]

    @when('@:0.8')
    def configure_args(self):
        """Configure arguments are passed using meson_args functions"""
        return [
            '--with-xkb-config-root={0}'.format(self.spec['xkbdata'].prefix),
            '--disable-docs',
            '--' + ('en' if self.spec.satisfies('+wayland') else 'dis') + 'able-wayland'
        ]

    @when('@:0.8')
    def meson(self, spec, prefix):
        """Run the AutotoolsPackage configure phase in source_path"""
        configure('--prefix=' + prefix, *self.configure_args())

    @when('@:0.8')
    def build(self, spec, prefix):
        """Run the AutotoolsPackage build phase in source_path"""
        make()

    @when('@:0.8')
    def install(self, spec, prefix):
        """Run the AutotoolsPackage install phase in source_path"""
        make('install')
