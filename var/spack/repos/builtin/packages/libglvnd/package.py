# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libglvnd(AutotoolsPackage):
    """The GL Vendor-Neutral Dispatch library

    libglvnd is a vendor-neutral dispatch layer for arbitrating OpenGL API calls
    between multiple vendors. It allows multiple drivers from different vendors
    to coexist on the same filesystem, and determines which vendor to dispatch
    each API call to at runtime.

    Both GLX and EGL are supported, in any combination with OpenGL and OpenGL
    ES."""

    homepage = "https://github.com/NVIDIA/libglvnd"
    url      = ("https://github.com/NVIDIA/libglvnd/releases/download"
                "/v1.1.1/libglvnd-1.1.1.tar.gz")
    git      = "https://github.com/NVIDIA/libglvnd.git"

    version('master', branch='master')

    version('1.1.1', sha256='71918ed1261e4eece18c0b74b50dc62c'
                            '0237b8d526e83277ef078554544720b9')
    version('1.1.0', sha256='f5a74598e769d55d652c464cb6507437'
                            'dac5c2d513f16c6ddf3a1bec655a1824')

    variant('egl', default=True, description="Enable OpenGL EGL support.")
    variant('glx', default=True, description="Enable GLX support.")
    variant('gles', default=True, description="Enable OpenGL ES support.")

    # TODO(opadron): Should any of these virtuals be limited in version?
    # TODO(opadron): If so, which and what versions?
    provides('gl')
    provides('glx', when='+glx')
    provides('egl', when='+egl')
    provides('gles', when='+gles')

    depends_on('libxext')
    depends_on('libx11')
    depends_on('glproto')

    @when('@master')
    def autoreconf(self, spec, prefix):
        autogen = Executable('./autogen.sh')
        autogen()

    def configure_args(self):
        args = []
        if '+egl' in self.spec: args.append('--enable-egl')
        if '+glx' in self.spec: args.append('--enable-glx')
        if '+gles' in self.spec: args.append('--enable-gles')

        if '~egl' in self.spec: args.append('--disable-egl')
        if '~glx' in self.spec: args.append('--disable-glx')
        if '~gles' in self.spec: args.append('--disable-gles')

        return args
