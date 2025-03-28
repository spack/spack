# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *
from spack.pkg.builtin.apple_gl import AppleGlBase


class AppleGlu(AppleGlBase):
    """Shim package for Apple implementation of OpenGL Utility Libray (GLU)"""

    version("1.3.0")

    provides("glu@1.3")

    depends_on("apple-clang", type="build")
    requires("platform=darwin", msg="Apple-GL is only available on Darwin, when using Apple Clang")
