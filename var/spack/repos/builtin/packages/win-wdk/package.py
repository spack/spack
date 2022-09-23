
# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import re

from lib.spack.spack.directives import depends_on
from spack.package import *


class Wdk(Package):

    executables = ["mt"]
    version("10.0.19041.0", sha256="", url="")
    version("10.0.18362.0", sha256="", url="")
    version("10.0.17763.0", sha256="", url="")
    version("10.0.17134.0", sha256="", url="")
    version("10.0.16299.0", sha256="", url="")
    version("10.0.15063.0", sha256="", url="")
    version("10.0.14393.0", sha256="", url="")
    version("10.0.10586.0", sha256="", url="")
    version("10.0.26639.0", sha256="", url="")

    depends_on("winsdk@10.0.19041.0", when="@10.0.19041.0")
    depends_on("winsdk@10.0.18362.0", when="@10.0.18362.0")
    depends_on("winsdk@10.0.17763.0", when="@10.0.17763.0")
    depends_on("winsdk@10.0.17134.0", when="@10.0.17134.0")
    depends_on("winsdk@10.0.16299.0", when="@10.0.16299.0")
    depends_on("winsdk@10.0.15063.0", when="@10.0.15063.0")
    depends_on("winsdk@10.0.14393.0", when="@10.0.14393.0")
    depends_on("winsdk@10.0.10586.0", when="@10.0.10586.0")
    depends_on("winsdk@10.0.26639.0", when="@10.0.26639.0")

    for plat in ["linux", "darwin", "cray"]:
        conflicts("platform=%s" % plat)

    @classmethod
    def determine_version(cls, exe):
        """
        WDK is a set of drivers that we would like to
        be discoverable externally by Spack.
        The executable does not provide the WDK
        version so we derive from the exe path
        """
        version_match_pat = re.compile(r"[0-9][0-9].[0-9]+.[0-9][0-9][0-9][0-9][0-9]")
        ver_str = re.search(version_match_pat, exe)
        return ver_str if not ver_str else Version(ver_str.group())

    def setup_dependent_environment(self):
        os.environ["WDKContentRoot"] = self.prefix

    def install(self, spec, prefix):
        install_args = ["/features", "+", "/quiet", "/installpath", self.prefix]
        with working_dir(self.stage.source_dir):
            Executable("wdksetup.exe")(*install_args)