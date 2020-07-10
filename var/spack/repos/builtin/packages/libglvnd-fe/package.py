# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LibglvndFe(BundlePackage):
    """The GL Vendor-Neutral Dispatch library (Frontend Dummy Package)

    libglvnd is a vendor-neutral dispatch layer for arbitrating OpenGL API
    calls between multiple vendors. It allows multiple drivers from different
    vendors to coexist on the same filesystem, and determines which vendor to
    dispatch each API call to at runtime.

    Both GLX and EGL are supported, in any combination with OpenGL and OpenGL
    ES."""

    homepage = "https://github.com/NVIDIA/libglvnd"

    version('1.1.1', sha256='71918ed1261e4eece18c0b74b50dc62c0237b8d526e83277ef078554544720b9')

    variant('glx', default=False, description='Provide GLX API')
    variant('egl', default=False, description='Provide EGL API')

    depends_on('libglvnd')

    depends_on('libglvnd-be-gl')
    depends_on('libglvnd-be-glx', when='+glx')
    depends_on('libglvnd-be-egl', when='+egl')

    provides('gl')
    provides('glx', when='+glx')
    provides('egl', when='+egl')

    @property
    def gl_libs(self):
        return find_libraries('libOpenGL',
                              root=self.spec['libglvnd'].prefix,
                              shared=True,
                              recursive=True)

    @property
    def glx_libs(self):
        return find_libraries('libGLX',
                              root=self.spec['libglvnd'].prefix,
                              shared=True,
                              recursive=True)

    @property
    def egl_libs(self):
        return find_libraries('libEGL',
                              root=self.spec['libglvnd'].prefix,
                              shared=True,
                              recursive=True)
