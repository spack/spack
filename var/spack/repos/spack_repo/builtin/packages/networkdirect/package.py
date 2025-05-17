# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

import spack.build_systems.msbuild as msbuild
from spack.package import *


class Networkdirect(MSBuildPackage):
    """NetworkDirect is a user-mode programming interface specification
    for Remote Direct Memory Access (RDMA)"""

    homepage = "https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/hh997033(v=ws.11)"
    url = "https://github.com/microsoft/NetworkDirect/archive/refs/tags/v2.0.zip"

    maintainers("johnwparent")

    license("MIT", checked_by="johnwparent")

    version("2.0", sha256="ba05a9be32ff39e08766c5a726ee63d47ee3eb9cab53b2b4b656de2d9158460c")

    requires("platform=windows")

    depends_on("cxx")
    requires("%msvc")

    depends_on("win-sdk")
    depends_on("win-wdk")

    # Networkdirect uses a build system called CBT that is built on top of MSBuild
    # CBT is entirely deprecated, and fully incompatible with modern dotnet versions
    # so we disable the CBT system and drive the underlying MSBuild system directly
    patch("no_cbt.patch")


class MSBuildBuilder(msbuild.MSBuildBuilder):

    build_targets = ["ndutil"]

    # Networkdirect is a unique package where providing
    # typically required information actually
    # breaks expected behavior, override the defaults
    @property
    def std_msbuild_args(self):
        return []

    def msbuild_args(self):
        args = ["-noLogo"]
        args.append(
            self.define("WindowsTargetPlatformVersion", str(self.pkg["win-sdk"].version) + ".0")
        )
        # one of the headers we need isn't generated during release builds
        args.append(self.define("Configuration", "Debug"))
        args.append("src\\netdirect.sln")
        return args

    def install(self, pkg, spec, prefix):
        base_build = pkg.stage.source_path
        out = os.path.join(base_build, "out")
        build_configuration = glob.glob(os.path.join(out, "*"))[0]
        for x in glob.glob(os.path.join(build_configuration, "**", "*.lib")):
            install_path = x.replace(build_configuration, prefix)
            mkdirp(os.path.dirname(install_path))
            install(x, install_path)
        include_dir = os.path.join(build_configuration, "include")
        install_tree(include_dir, prefix.include)
        # for whatever reason this header is not moved to the "out" prefix
        # with the rest of the headers, ensure its there
        install(os.path.join(base_build, "src", "ndutil", "ndsupport.h"), prefix.include)
