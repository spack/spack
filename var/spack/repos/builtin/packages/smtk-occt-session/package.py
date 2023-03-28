# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SmtkOcctSession(CMakePackage):
    """SMTK Plugin for working with Models using OpenCascade"""

    homepage = "https://www.computationalmodelbuilder.org/"
    url = "https://gitlab.kitware.com/cmb/plugins/opencascade-session"
    git = "https://gitlab.kitware.com/cmb/plugins/opencascade-session.git"

    maintainers = ["kwryankrattiger"]

    # Versions
    version("master", branch="master", submodules=False)
    version("2022.08.11", commit="797488203e073b3fccc0cdf038c11e1f347ab858", submodules=False)

    # Variants
    variant("enable_by_default", default=False, description="Enable plugin by default")
    variant("testing", default=False, description="Enable testing")

    # Dependencies
    depends_on("smtk")
    depends_on("opencascade@7.4.0p1")
    depends_on("boost +filesystem")
    depends_on("nlohmann-json")

    # Cannot have VTK and ParaView in the same stack
    depends_on("opencascade ~vtk", when="^smtk +paraview")

    def setup_run_environment(self, env):
        if "smtk +paraview" in self.spec and "+enable_by_default" in self.spec:
            for config_file in find(self.prefix, "smtk.opencascadesession.xml"):
                env.prepend_path("PV_PLUGIN_CONFIG_FILE", config_file)

    def cmake_args(self):
        args = [
            self.define_from_variant("OPENCASCADE_ENABLE_TESTING", "testing"),
            self.define("OCCT_DIR", self.spec["opencascade"].prefix),
        ]
        return args
