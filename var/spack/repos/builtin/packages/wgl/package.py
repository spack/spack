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
    libraries = ["OpenGL32.Lib"]

    # versions here are in no way related to actual WGL versions (there is only one on a system at a time)
    # but instead reflects the Windows Kit version that a particular WGL library file is found in
    # Windows Kits are intended to be more or less contained environments so this allows us to
    # marshall our SDK and WDK to their respective WGLs. The purpose here is to better reflect
    # the concept of an MS build toolchain version W.R.T. to MSVC
    version("10.0.19041")
    version("10.0.18362")
    version("10.0.17763")
    version("10.0.17134")
    version("10.0.16299")
    version("10.0.15063")
    version("10.0.14393")
    version("10.0.10586")
    version("10.0.26639")

    # As per https://github.com/spack/spack/pull/31748 this provisory version represents
    # an arbitrary openGL version designed for maximum compatibility with calling packages
    # this current version simply reflects the latest OpenGL vesion available at the time of
    # package creation and is set in a way that all specs currently depending on GL are satisfied appropriately
    provides("gl@4.6")

    # WGL exists on all Windows systems post win 98, however the headers
    # needed to use OpenGL are found in the SDK (GL/gl.h)
    # Dep is needed to consolidate sdk version to locate header files for
    # version of SDK being used
    depends_on("win-sdk")

    # WGL has no meaning on other platforms, should not be able to spec
    for plat in ["linux", "darwin", "cray"]:
        conflicts("platform=%s" % plat)

    @classmethod
    def determine_version(cls, lib):
        """Allow for WGL to be externally detectable"""
        version_match_pat = re.compile(r"[0-9][0-9].[0-9]+.[0-9][0-9][0-9][0-9][0-9]")
        ver_str = re.search(version_match_pat, lib)
        return ver_str if not ver_str else Version(ver_str.group())

    # As noted above, the headers neccesary to include
    @property
    def headers(self):
        return find_headers("GL/gl.h", root=self.spec["win-sdk"].prefix.includes, recursive=True)

    # We use the dll to determine existence, but on Windows we link against the .lib
    # associated with the .dll
    @property
    def libs(self):
        return find_libraries("opengl32", shared=False, root=self.prefix, recursive=True)
