# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import re

from spack.package import *


class WinSdk(Package):
    """
    Windows Desktop C++ development SDK
    Spack packaged used to define search heuristics
    to locate the SDK on a filesystem
    """

    homepage = "https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/"
    has_code = False

    # The sdk has many libraries and executables. Record one for detection purposes
    libraries = ["rcdll.dll"]

    version("10.0.19041")
    version("10.0.18362")
    version("10.0.17763")
    version("10.0.17134")
    version("10.0.16299")
    version("10.0.15063")
    version("10.0.14393")
    version("10.0.10586")
    version("10.0.26639")

    # WinSDK versions depend on compatible compilers
    # WDK versions do as well, but due to their one to one dep on the SDK
    # we can ensure that requirment here
    # depends_on("%msvc:", when="@10.")

    # For now we don't support Windows development env
    # on other platforms
    for plat in ["linux", "darwin", "cray"]:
        conflicts("platform=%s" % plat)

    @classmethod
    def determine_version(cls, lib):
        """
        WinSDK that we would like to
        be discoverable externally by Spack.
        """
        # This version is found in the package's path
        # not by calling an exe or a libraries name
        version_match_pat = re.compile(r"[0-9][0-9].[0-9]+.[0-9][0-9][0-9][0-9][0-9]")
        ver_str = re.search(version_match_pat, lib)
        return ver_str if not ver_str else Version(ver_str.group())

    def install(self, spec, prefix):
        raise RuntimeError(
            "This package is not installable from Spack\
            and should be installed on the system prior to Spack use.\
                If not installed this package should be installed via\
                    the Visual Studio installer in order to use the \
                        MSVC compiler on Windows."
            "If absolutely neccesary this SDK can be installed directly from Microsoft\
                but this approach is not recommended unless you know what you're doing \
                    or if you're on Windows 11 you have no choice for the moment."
        )
