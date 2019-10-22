# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libglvnd(AutotoolsPackage):
    """The GL Vendor-Neutral Dispatch library

    libglvnd is a vendor-neutral dispatch layer for arbitrating OpenGL API
    calls between multiple vendors. It allows multiple drivers from different
    vendors to coexist on the same filesystem, and determines which vendor to
    dispatch each API call to at runtime.

    Both GLX and EGL are supported, in any combination with OpenGL and OpenGL
    ES."""

    homepage = "https://github.com/NVIDIA/libglvnd"
    url      = "https://github.com/NVIDIA/libglvnd/releases/download/v1.1.1/libglvnd-1.1.1.tar.gz"
    git      = "https://github.com/NVIDIA/libglvnd.git"

    version('master', branch='master')

    version('1.1.1', sha256='71918ed1261e4eece18c0b74b50dc62c0237b8d526e83277ef078554544720b9')

    conflicts('platform=darwin', msg='libglvnd is linux specific')
    conflicts('platform=bgq', msg='libglvnd is linux specific')

    depends_on('libxext')
    depends_on('libx11')
    depends_on('glproto')

    @when('@master')
    def autoreconf(self, spec, prefix):
        autogen = Executable('./autogen.sh')
        autogen()

    def configure_args(self):
        return [
            '--enable-egl',
            '--enable-gles',
            '--enable-glx'
        ]
