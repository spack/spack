# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Glm(CMakePackage):
    """OpenGL Mathematics (GLM) is a header only C++ mathematics library for
    graphics software based on the OpenGL Shading Language (GLSL) specification
    """

    homepage = "https://github.com/g-truc/glm"
    url = "https://github.com/g-truc/glm/archive/0.9.7.1.tar.gz"

    version('0.9.7.1', '61af6639cdf652d1cdd7117190afced8')

    depends_on('cmake@2.6:', type='build')
