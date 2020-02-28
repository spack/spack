# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install opensubdiv
#
# You can edit this file again by typing:
#
#     spack edit opensubdiv
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Opensubdiv(CMakePackage):
    """OpenSubdiv is a set of open source libraries that implement high 
    performance subdivision surface (subdiv) evaluation on massively parallel CPU
    and GPU architectures. This code path is optimized for drawing deforming
    surfaces with static topology at interactive framerates."""

    homepage = "http://graphics.pixar.com/opensubdiv/docs/intro.html"
    url      = "https://github.com/PixarAnimationStudios/OpenSubdiv/archive/v3_4_0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('3_4_0',     sha256='d932b292f83371c7518960b2135c7a5b931efb43cdd8720e0b27268a698973e4')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
