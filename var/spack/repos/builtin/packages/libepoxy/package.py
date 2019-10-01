# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libepoxy(AutotoolsPackage):
    """Epoxy is a library for handling OpenGL function pointer management for
    you."""
    homepage = "https://github.com/anholt/libepoxy"
    url      = "https://github.com/anholt/libepoxy/releases/download/1.4.3/libepoxy-1.4.3.tar.xz"
    list_url = "https://github.com/anholt/libepoxy/releases"

    version('1.4.3', 'af4c3ce0fb1143bdc4e43f85695a9bed')
    version('1.3.1', '96f6620a9b005a503e7b44b0b528287d')

    depends_on('pkgconfig', type='build')
    depends_on('meson')
    depends_on('gl')
    depends_on('libx11', when='+glx')

    variant('glx', default=True, description='enable GLX support')

    def configure_args(self):
        # Disable egl, otherwise configure fails with:
        # error: Package requirements (egl) were not met
        # Package 'egl', required by 'virtual:world', not found
        args = ['--enable-egl=no']

        # --enable-glx defaults to auto and was failing on PPC64LE systems
        # because libx11 was missing from the dependences. This explicitly
        # enables/disables glx support.
        if '+glx' in self.spec:
            args.append('--enable-glx=yes')
        else:
            args.append('--enable-glx=no')

        return args
