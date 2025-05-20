# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import re
import sys

from spack_repo.builtin.build_systems import msbuild

from spack.package import *


class Msmpi(msbuild.MSBuildPackage):
    """MSMPI is a Windows port of MPICH provided by the Windows team"""

    homepage = "https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi"
    url = "https://github.com/microsoft/Microsoft-MPI/archive/refs/tags/v10.1.1.tar.gz"
    git = "https://github.com/microsoft/Microsoft-MPI.git"
    tags = ["windows"]

    executables = ["mpiexec"]

    version("10.1.1", sha256="63c7da941fc4ffb05a0f97bd54a67968c71f63389a0d162d3182eabba1beab3d")
    version("10.0.0", sha256="cfb53cf53c3cf0d4935ab58be13f013a0f7ccb1189109a5b8eea0fcfdcaef8c1")

    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    provides("mpi")

    depends_on("c", type="build")

    depends_on("win-wdk")
    depends_on("networkdirect")
    depends_on("perl")

    # MSMPI's build system is hard coded to assume
    # paths to gfortran and network direct
    # This patch makes the build compatible with
    # ifort/ifx and allows for a dynamically located
    # network direct install
    patch("ifort_nd_compat.patch")
    # the cbt msbuild extension ms-mspi's build sytem
    # uses has been removed. This patch removes the
    # associated functionality from the build system
    patch("burn_cbt.patch")
    # For whatever reason, specifying the platform toolset
    # prevents message compiler (mc) detection
    # We know its present because we have a WDK
    # patches the build system to just directly call the MC
    patch("no_mc.patch")

    requires("platform=windows")
    requires("%msvc")

    @classmethod
    def determine_version(cls, exe):
        # MSMPI is typically MS only, don't detect on other platforms
        # to avoid potential collisions with other mpiexec executables
        if sys.platform != "win32":
            return None
        output = Executable(exe)(output=str, error=str)
        ver_str = re.search(r"Microsoft MPI Startup Program \[Version ([0-9.]+)\]", output)
        return Version(ver_str.group(1)) if ver_str else None

    def setup_dependent_package(self, module, dependent_spec):
        # MSMPI does not vendor compiler wrappers, instead arguments should
        # be manually supplied to compiler by consuming package
        # Note: This is not typical of MPI installations
        self.spec.mpicc = dependent_spec["c"].package.cc
        self.spec.mpicxx = dependent_spec["cxx"].package.cxx
        if "fortran" in dependent_spec:
            self.spec.mpifc = dependent_spec["fortran"].package.fc
            self.spec.mpif77 = dependent_spec["fortran"].package.f77


class MSBuildBuilder(msbuild.MSBuildBuilder):
    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        # os.path.join interprets C: as an indicator of a relative path
        # so we need to use the traditional string join here
        ifort_root = "\\".join(self.pkg.compiler.fc.split(os.path.sep)[:-2])
        env.set("SPACK_IFORT", ifort_root)
        env.prepend_path("IncludePath", self.spec["networkdirect"].prefix.include)
        env.set("ND_DIR", self.spec["networkdirect"].prefix.ndutil)

    @property
    def std_msbuild_args(self):
        return []

    # We will need to burn out the CBT build system and associated files
    # and instead directly invoke msbuild per sln we're interested in
    # and generate our own installer
    def msbuild_args(self):
        pkg = self.pkg
        args = ["-noLogo"]
        ifort_bin = '"' + os.path.dirname(pkg.compiler.fc) + '"'
        args.append(self.define("IFORT_BIN", ifort_bin))
        args.append(self.define("PlatformToolset", "v" + pkg["msvc"].platform_toolset_ver))
        args.append(self.define("VCToolsVersion", pkg["msvc"].msvc_version))
        args.append(
            self.define("WindowsTargetPlatformVersion", str(pkg["win-sdk"].version) + ".0")
        )
        args.append(self.define("Configuration", "Release"))
        args.append("src\\msmpi.sln")
        return args

    def install(self, pkg, spec, prefix):
        base_build = pkg.stage.source_path
        out = os.path.join(base_build, "out")
        build_configuration = glob.glob(os.path.join(out, "*"))[0]
        for x in glob.glob(os.path.join(build_configuration, "**", "*.*")):
            install_path = x.replace(build_configuration, prefix)
            mkdirp(os.path.dirname(install_path))
            install(x, install_path)
        include_dir = os.path.join(os.path.join(base_build, "src"), "include")
        install_tree(include_dir, prefix.include)
