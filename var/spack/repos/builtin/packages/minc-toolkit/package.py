# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class MincToolkit(CMakePackage):
    """Bundles multiple MINC-related packages"""

    homepage = "https://github.com/BIC-MNI/minc-toolkit-v2"
    git      = "https://github.com/BIC-MNI/minc-toolkit-v2.git"

    version('1.9.18.1', commit="38597c464b6e93eda680ab4a9e903366d53d7737",
            submodules=True)

    variant('shared', default=True,
            description="Build shared libraries")
    variant('visualisation', default=False,
            description="Build visual tools (Display, register, etc.)")

    depends_on('perl')
    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('zlib', type='link')
    depends_on('freeglut', when="+visualisation")

    def cmake_args(self):
        return [self.define_from_variant('MT_BUILD_SHARED_LIBS', 'shared'),
                self.define_from_variant('MT_BUILD_VISUAL_TOOLS', 'visualisation'),
                # newer ANTs packaged separately
                "-DMT_BUILD_ANTS=OFF",
                # build error; should package newer c3d separately
                "-DMT_BUILD_C3D=OFF",
                # should be packaged separately with newer ITK
                "-DMT_BUILD_ELASTIX=OFF"
                ]
