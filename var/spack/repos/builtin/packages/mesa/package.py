##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import inspect


class Mesa(AutotoolsPackage):
    """Mesa is an open-source implementation of the OpenGL
    specification - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"
    url      = "https://mesa.freedesktop.org/archive/12.0.3/mesa-12.0.3.tar.xz"
    list_url = "https://mesa.freedesktop.org/archive"
    list_depth = 2

    version('17.1.1', 'a4844bc6052578574f9629458bcbb749')
    version('13.0.6', '1e5a769bc6cfd839cf3febcb179c27cc')
    version('12.0.3', '1113699c714042d8c4df4766be8c57d8')

    variant('dri', default=False,
            description="Use DRI drivers for accelerated OpenGL rendering")
    variant('llvm', default=False,
            description="Build DRI drivers that depend on llvm")

    # NOTE: mesa@12+dri may not build on older platforms,
    #       due to dependency on libudev or libsysfs.
    #       The dependency has been removed from mesa@13 onwards.

    # General dependencies
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('flex@2.5.35:', type='build')
    depends_on('bison@2.4.1:', type='build')
    depends_on('binutils', type='build')
    depends_on('python@2.6.4:', type='build')
    depends_on('py-mako@0.3.4:', type='build')
    depends_on('gettext')
    depends_on('icu4c')
    depends_on('expat')
    depends_on('libpthread-stubs')
    depends_on('openssl')
    depends_on('xproto')
    depends_on('glproto@1.4.14:')
    depends_on('presentproto@1.0:')
    depends_on('libxcb@1.9.3:')
    depends_on('libx11')
    depends_on('libxext')
    depends_on('libxshmfence@1.1:')
    depends_on('libxdamage')
    depends_on('libxfixes')
    depends_on('libxv')
    depends_on('libxvmc')

    # For DRI and hardware acceleration
    depends_on('libdrm', when='+dri')
    depends_on('dri2proto@2.6:', type='build', when='+dri')
    depends_on('dri3proto@1.0:', type='build', when='+dri')
    depends_on('llvm@:3.8.1+link_dylib', when='@12:12.99+dri+llvm')
    depends_on('llvm@:3.9.1+link_dylib', when='@13:13.99+dri+llvm')
    depends_on('llvm+link_dylib', when='@14:17.99+dri+llvm')
    depends_on('libelf', when='+dri+llvm')

    # For optional features, possible new variants:
    #depends_on('libgcrypt')
    #depends_on('nettle')

    def configure_args(self):
        spec = self.spec
        args = ['--enable-texture-float', '--enable-xa', '--enable-glx-tls']
        if '+dri' in spec:
            # Build gallium drivers for platforms supported by spack;
            # exclude drivers for embedded systems:
            #   vc4, freedreno, etnaviv, imx
            args.extend(['--with-egl-platforms=x11,drm',
                         '--disable-osmesa', '--enable-gallium-osmesa'])
            gallium = 'svga,i915,r600,nouveau,swrast,virgl'
            if spec.satisfies('@:16.99'):
                # ilo driver removed in @17:
                gallium += ',ilo'
            if '+llvm' in spec:
                gallium += ',r300,radeonsi,swr'
            args.extend(['--with-gallium-drivers=' + gallium])
        else:
            args.extend(['--disable-dri', '--disable-egl',
                         '--without-gallium-drivers', '--enable-osmesa'])
        return args
