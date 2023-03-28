# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Modelbuilder(CMakePackage):
    """Modelbuilder is an open-source ParaView Client
    with Simulation pre-processing workflow tools.
    """

    homepage = "https://www.computationalmodelbuilder.org"
    url = "https://gitlab.kitware.com/cmb/cmb"
    git = "https://gitlab.kitware.com/cmb/cmb.git"

    maintainers = ["kwryankrattiger"]

    version("master", branch="master")

    releases = [
        "22.04.0",
        "21.12.0",
        "21.07.0",
        "21.05.0",
    ]
    for ver in releases:
        version(ver, branch="v{0}".format(ver), submodules=False)

    variant("doc", default=False, description="Build documentation.")
    variant("python", default=True, description="Enable built-in Python shell.")
    variant("remote", default=False, description="Enable remote rendering support.")
    variant("shared", default=True, description="Build with shared libs.")
    variant("smtk", default=True, description="Enable Built-in SMTK plugins.")

    depends_on("smtk +paraview +qt", when="+smtk")
    depends_on("smtk +shared", when="+smtk +shared")
    depends_on("paraview +qt")
    depends_on("paraview +shared", when="+shared")
    depends_on("paraview +python3", when="+python")
    depends_on("python@3:", when="+python")
    depends_on("qt@5: +gui")
    depends_on("py-sphinx", when="+doc")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("cmb_enable_pythonshell", "python"),
            self.define_from_variant("cmb_enable_multiservers", "remote"),
            self.define_from_variant("cmb_enable_documentation", "doc"),
            # self.define_from_variant("cmb_enable_objectpicking", "smtk"),
        ]
        return args
