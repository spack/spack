# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cairo(AutotoolsPackage):
    """Cairo is a 2D graphics library with support for multiple output
    devices."""

    homepage = "https://www.cairographics.org/"
    url      = "https://www.cairographics.org/releases/cairo-1.16.0.tar.xz"

    version('1.16.0', sha256='5e7b29b3f113ef870d1e3ecf8adf21f923396401604bda16d44be45e66052331')
    version('1.14.12', '490025a0ba0622a853010f49fb6343f29fb70b9b')
    version('1.14.8', 'c6f7b99986f93c9df78653c3e6a3b5043f65145e')
    version('1.14.0', '53cf589b983412ea7f78feee2e1ba9cea6e3ebae')

    variant('X', default=False, description="Build with X11 support")
    variant('pdf', default=False, description="Enable cairo's PDF surface backend feature")
    variant('gobject', default=False, description="Enable cairo's gobject functions feature")

    depends_on('libx11', when='+X')
    depends_on('libxext', when='+X')
    depends_on('libxrender', when='+X')
    depends_on('libxcb', when='+X')
    depends_on('python', when='+X', type='build')
    depends_on('libpng')
    depends_on('glib')
    depends_on('pixman')
    depends_on('freetype')
    depends_on('pkgconfig', type='build')
    depends_on('fontconfig@2.10.91:')  # Require newer version of fontconfig.

    def configure_args(self):
        args = [
            '--disable-trace',  # can cause problems with libiberty
            '--enable-tee'
        ]

        if '+X' in self.spec:
            args.extend(['--enable-xlib', '--enable-xcb'])
        else:
            args.extend(['--disable-xlib', '--disable-xcb'])

        args.extend(self.enable_or_disable('pdf'))
        args.extend(self.enable_or_disable('gobject'))

        return args
