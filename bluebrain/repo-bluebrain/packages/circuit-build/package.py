# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CircuitBuild(PythonPackage):
    """Command Line API for building circuits"""

    homepage = "https://bbpgitlab.epfl.ch/nse/circuit-build"
    git = "ssh://git@bbpgitlab.epfl.ch/nse/circuit-build.git"

    version("develop", branch="main")
    version("4.1.0", tag="circuit-build-v4.1.0")

    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-pyyaml@5.0:", type=("build", "run"))
    depends_on("snakemake@6.0:", type=("build", "run"))
    depends_on("py-jsonschema@3.2.0:", type=("build", "run"))
    depends_on("py-jinja2@2.10.0:", type=("build", "run"))

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.spec["snakemake"].prefix.bin)
