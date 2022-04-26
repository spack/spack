# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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

    # CMake tries to download a retired version of zlib (minc-toolkit-v2/#146),
    # but the build fails with USE_SYSTEM_ZLIB and updating minc-toolkit to a newer
    # commit where this issue is fixed triggers a build failure on Ubuntu
    # (minc-toolkit-v2/#147)
    patch('https://github.com/BIC-MNI/minc-toolkit-v2/commit/c7ebff42838e083e9368caebff87778d6ea27427.patch?full_index=1',
          sha256="42ee1d500553369a21720f18cef77b7905ef29a4f47ef8adce24c8adafbea74f")

    variant('shared', default=True,
            description="Build shared libraries")
    variant('visualisation', default=False,
            description="Build visual tools (Display, register, etc.)")

    depends_on('perl')
    # included Perl packages are not added to the Perl path by default.
    # rather than inheriting from both CMakePackage and PerlPackage,
    # it seems clean just to add them as dependencies:
    depends_on('perl-text-format', type=('build', 'run'))
    depends_on('perl-getopt-tabular', type=('build', 'run'))
    depends_on('perl-mni-perllib', type=('build', 'run'))
    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('zlib', type='link')
    depends_on('freeglut', when="+visualisation")

    def cmake_args(self):
        return [self.define_from_variant('MT_BUILD_SHARED_LIBS', 'shared'),
                self.define_from_variant('MT_BUILD_VISUAL_TOOLS', 'visualisation'),
                # newer ANTs packaged separately
                "-DMT_BUILD_ANTS=OFF",
                # newer c3d packaged separately
                "-DMT_BUILD_C3D=OFF",
                # should be packaged separately with newer ITK
                "-DMT_BUILD_ELASTIX=OFF"
                ]
