# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack import *


class MesaDemos(AutotoolsPackage):
    """This package provides some demo applications for testing Mesa."""

    homepage = "https://www.mesa3d.org"
    url      = "https://github.com/freedesktop/mesa-demos/archive/mesa-demos-8.3.0.tar.gz"

    version('8.3.0', sha256='9bc1b37f4fc7bfc3f818f2d3851ffde28e8167ef11dca87f4781e9ef6206901f')
    version('8.2.0', sha256='5a9f71b815d968d0c3b77edfcc3782d0211f8520b00da9e554ccfed80c8889f6')
    version('8.1.0', sha256='cc5826105355830208c90047fc38c5b09fa3ab0045366e7e859104935b00b76d')

    variant('osmesa', default=False, description="Enable the OSMesa frontend.")

    is_linux = sys.platform.startswith('linux')
    variant('glx', default=is_linux, description="Enable the GLX frontend.")

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')
    depends_on('pkgconfig', type='build')

    depends_on('gl')
    depends_on('glx', when='+glx')
    depends_on('libx11',  when='+glx')
    depends_on('libxext', when='+glx')
    depends_on('osmesa', when='+osmesa')

    depends_on('mesa-glu')
    depends_on('freeglut')
    depends_on('glew@1.5.4:')

    def configure_args(self):
        spec = self.spec

        args = [
            "--disable-egl",
            "--disable-gles1",
            "--disable-gles2",
            "--disable-vg",
            "--disable-libdrm",
            "--disable-wayland",
            "--disable-gbm",
            "--disable-freetype2",
            "--disable-rbug"
        ]

        args.extend(self.enable_or_disable('osmesa'))

        if '+glx' in spec:
            args.append('--enable-x11')
        else:
            args.append('--disable-x11')

        return args
