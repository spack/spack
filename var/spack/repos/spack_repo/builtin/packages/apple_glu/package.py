# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin.packages.apple_gl.package import AppleGlBase

from spack.package import *


class AppleGlu(AppleGlBase):
    """Shim package for Apple implementation of OpenGL Utility Libray (GLU)"""

    version("1.3.0")

    provides("glu@1.3")

    requires("platform=darwin", msg="Apple-GL is only available on Darwin")
