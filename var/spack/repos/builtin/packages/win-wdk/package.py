# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import re

from spack.package import *


class WinWdk(Package):

    homepage = "https://learn.microsoft.com/en-us/windows-hardware/drivers/"


    executables = ["mt"]



    version("10.0.19041", sha256="5F4EA0C55AF099F97CB569A927C3A290C211F17EDCFC65009F5B9253B9827925", url="https://go.microsoft.com/fwlink/?linkid=2128854", expand=False)
    version("10.0.18362", sha256="C35057CB294096C63BBEA093E5024A5FB4120103B20C13FA755C92F227B644E5", url="https://go.microsoft.com/fwlink/?linkid=2085767", expand=False)
    version("10.0.17763", sha256="E6E5A57BF0A58242363CD6CA4762F44739F19351EFC06CAD382CCA944B097235", url="https://go.microsoft.com/fwlink/?linkid=2026156", expand=False)
    version("10.0.17134", sha256="48E636117BB7BFE66B1ADE793CC8E885C42C880FADAEE471782D31B5C4D13E9B", url="https://go.microsoft.com/fwlink/?linkid=873060", expand=False)
    version("10.0.16299", sha256="14EFBCC849E5977417E962F1CD68357D21ABF27393110B9D95983AD03FC22EF4", url="https://go.microsoft.com/fwlink/p/?linkid=859232", expand=False)
    version("10.0.15063", sha256="489B497111BC791D9021B3573BFD93086A28B598C7325AB255E81C6F5D80A820", url="https://go.microsoft.com/fwlink/p/?LinkID=845980", expand=False)
    version("10.0.14393", sha256="0BFB2AC9DB446E0D98C29EF7341A8C8E8E7AA24BC72B00C5704A88B13F48B3CB", url="https://go.microsoft.com/fwlink/p/?LinkId=526733", expand=False)

    # need one to one dep on SDK per https://github.com/MicrosoftDocs/windows-driver-docs/issues/1550
    depends_on("win-sdk@10.0.19041.0", when="@10.0.19041")
    depends_on("win-sdk@10.0.18362.0", when="@10.0.18362")
    depends_on("win-sdk@10.0.17763.0", when="@10.0.17763")
    depends_on("win-sdk@10.0.17134.0", when="@10.0.17134")
    depends_on("win-sdk@10.0.16299.0", when="@10.0.16299")
    depends_on("win-sdk@10.0.15063.0", when="@10.0.15063")
    depends_on("win-sdk@10.0.14393.0", when="@10.0.14393")


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
        # This points to all core build extensions needed to build
        # drivers on Windows
        os.environ["WDKContentRoot"] = self.prefix

    def install(self, spec, prefix):
        install_args = ["/features", "+", "/quiet", "/installpath", self.prefix]
        with working_dir(self.stage.source_dir):
            Executable("wdksetup.exe")(*install_args)
