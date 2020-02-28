# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Opensubdiv(CMakePackage):
    """OpenSubdiv is a set of open source libraries that implement high 
    performance subdivision surface (subdiv) evaluation on massively parallel CPU
    and GPU architectures. This code path is optimized for drawing deforming
    surfaces with static topology at interactive framerates."""

    homepage = "http://graphics.pixar.com/opensubdiv/docs/intro.html"
    url      = "https://github.com/PixarAnimationStudios/OpenSubdiv/archive/v3_4_0.tar.gz"

    version('3_4_0',     sha256='d932b292f83371c7518960b2135c7a5b931efb43cdd8720e0b27268a698973e4')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def cmake_args(self):
        args = []
        return args
