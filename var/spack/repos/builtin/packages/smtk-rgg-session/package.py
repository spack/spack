# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install smtk-rgg-session
#
# You can edit this file again by typing:
#
#     spack edit smtk-rgg-session
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------
from spack.package import *


class SmtkRggSession(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.computationalmodelbuilder.org/"
    url = "https://gitlab.kitware.com/cmb/plugins/rgg-session"
    git = "https://gitlab.kitware.com/cmb/plugins/rgg-session.git"

    maintainers = ["kwryankrattiger"]
    tags = ["cmb"]

    # Versions
    version("master", branch="master", submodules=False)
    version("2022.05.30", commit="f5ad1999323a9dd83ce5b3ee81dd3f9913d813dd", submodules=False)

    # Variants
    variant("python", default=True, description="Enable python wrappings")
    variant("enable_by_default", default=False, description="Enable plugin by default")

    # Dependencies
    depends_on("smtk +paraview +qt")
    depends_on("boost@1.64.0 +filesystem")
    depends_on("qt +gui")

    extends("python", when="+python")
    depends_on("python@3:", when="+python")

    def setup_run_environment(self, env):
        if "smtk +paraview" in self.spec and "+enable_by_default" in self.spec:
            for config_file in find(self.prefix, "smtk.rggsession.xml"):
                env.prepend_path("PV_PLUGIN_CONFIG_FILE", config_file)

    def cmake_args(self):
        args = [
            self.define_from_variant("RGG_ENABLE_PYTHON_WRAPPING", "python"),
            self.define_from_variant("ENABLE_PLUGIN_BY_DEFAULT", "enable_by_default"),
        ]
        return args
