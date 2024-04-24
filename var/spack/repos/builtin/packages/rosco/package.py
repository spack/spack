# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rosco(CMakePackage):
    """
    ROSCO controls package for OpenFAST from NREL
    Note: this only builds ROSCO controls library for inclusion with OpenFAST
    If the toolbox or tuning scripts are needed, please build manually
    """

    homepage = "https://rosco.readthedocs.io/en/latest/"
    url = "https://github.com/NREL/ROSCO/archive/refs/tags/v.2.9.1.tar.gz"
    git = "https://github.com/NREL/ROSCO.git"

    maintainers("dzalkind", "ndevelder")

    version("develop", branch="develop")
    version("main", branch="main")
    version("2.9.1", sha256="c226f802fd641910e8f00d9e479cdb9ea5988a8ddb9c86c455c0ee952a842b36")

    variant("shared", default=False, description="Build shared libraries")
    variant("pic", default=False, description="Position independent code")

    root_cmakelists_dir = "rosco/controller"

    def cmake_args(self):
        spec = self.spec

        options = []

        options.extend(
            [
                self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
                self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            ]
        )

        return options

    def setup_run_environment(self, env):
        env.set("ROSCO_DISCON", self.prefix.lib + "/libdiscon.so")
        env.set("ROSCO_DISCON_DIR", self.prefix.lib)

    def flag_handler(self, name, flags):
        if name == "fflags" and self.compiler.fc.endswith("gfortran"):
            flags.extend(["-ffree-line-length-0"])

        return (None, None, flags)
