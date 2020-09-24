# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Freeglut(CMakePackage, SourceforgePackage):
    """FreeGLUT is a free-software/open-source alternative to the OpenGL
       Utility Toolkit (GLUT) library"""

    homepage = "http://freeglut.sourceforge.net/"
    sourceforge_mirror_path = "freeglut/freeglut-3.2.1.tar.gz"
    version('3.2.1', sha256='d4000e02102acaf259998c870e25214739d1f16f67f99cb35e4f46841399da68')
    version('3.0.0', sha256='2a43be8515b01ea82bcfa17d29ae0d40bd128342f0930cd1f375f1ff999f76a2')
    patch('common-gcc10.patch', when="@3.2.1: %gcc@10.0:")
    depends_on('gl')
    depends_on('glu')
    depends_on('libx11')
    depends_on('libxrandr')
    depends_on('libxi')
    depends_on('xrandr')
    depends_on('inputproto')
