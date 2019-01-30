# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fontconfig(AutotoolsPackage):
    """Fontconfig is a library for configuring/customizing font access"""
    homepage = "http://www.freedesktop.org/wiki/Software/fontconfig/"
    url      = "http://www.freedesktop.org/software/fontconfig/release/fontconfig-2.12.3.tar.gz"

    version('2.12.3', 'aca0c734c1a38eb3ba12b2447dd90ab0')
    version('2.12.1', 'ce55e525c37147eee14cc2de6cc09f6c')
    version('2.11.1', 'e75e303b4f7756c2b16203a57ac87eba')

    depends_on('freetype')
    depends_on('gperf', type='build', when='@2.12.2:')
    depends_on('libxml2')
    depends_on('pkgconfig', type='build')
    depends_on('font-util')

    def configure_args(self):
        font_path = join_path(self.spec['font-util'].prefix, 'share', 'fonts')

        return [
            '--enable-libxml2',
            '--disable-docs',
            '--with-default-fonts={0}'.format(font_path)
        ]

    @run_after('install')
    def system_fonts(self):
        # point configuration file to system-install fonts
        # gtk applications were failing to display text without this
        config_file = join_path(self.prefix, 'etc', 'fonts', 'fonts.conf')
        filter_file('<dir prefix="xdg">fonts</dir>',
                    '<dir prefix="xdg">fonts</dir><dir>/usr/share/fonts</dir>',
                    config_file)
