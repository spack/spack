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
    version("5.0.2", tag="circuit-build-v5.0.2")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-pyyaml@5.0:", type=("build", "run"))
    depends_on("snakemake@6.0:", type=("build", "run"))
    depends_on("py-jsonschema@3.2.0:", type=("build", "run"))

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.spec["snakemake"].prefix.bin)
