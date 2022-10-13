# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

from spack.package import *


class Wgl(BundlePackage):
    """External WGl and Windows OpenGL emulation representation in Spack"""

    homepage = "https://learn.microsoft.com/en-us/windows/win32/opengl/wgl-and-windows-reference"

    # hard code the extension as shared lib
    libraries = ["opengl32.dll"]

    # As per https://github.com/spack/spack/pull/31748 this version and it's provisory represent
    # an arbitrary openGL version designed for maximum compatibility with calling packages
    # this current version simply reflects the latest OpenGL vesion available at the time of
    # package creation and is set in a way that all specs currently depending on GL are satisfied appropriately
    version("4.6")

    provides("gl@4.6")

    # WGL exists on all Windows systems post win 98, however the headers
    # needed to use OpenGL are found in the SDK (GL/gl.h)
    # Dep is needed to consolidate sdk version to locate header files for
    # version of SDK being used
    depends_on("win-sdk")

    # WGL has no meaning on other platforms, should not be able to spec
    for plat in ["linux", "darwin", "cray"]:
        conflicts("platform=%s" % plat)


    def determine_version(self, exe):
        """Allow for WGL to be externally detectable"""

    # As noted above, the headers neccesary to include
    @property
    def headers(self):
        return find_headers("GL/gl.h", root=self.spec["win-sdk"].includes, recursive=True)

    # We use the dll to determine existence, but on Windows we link against the .lib
    # associated with the .dll
    @property
    def libs(self):
        return find_libraries("opengl32", shared=False, root=self.prefix, recursive=True)
