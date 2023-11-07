# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyBluepyopt(PythonPackage):
    """Bluebrain Python Optimisation Library"""

    homepage = "https://github.com/BlueBrain/BluePyOpt"
    pypi = "bluepyopt/bluepyopt-1.9.27.tar.gz"

    # NOTE : while adding new release check pmi_rank.patch compatibility
    version("1.14.4", sha256="7567fd736053250ca06030f67ad93c607b100c2b98df8dc588c26b64cb3e171c")

    # patch required to avoid hpe-mpi linked mechanism library
    patch("pmi_rank.patch")

    variant("scoop", default=False, description="Use BluePyOpt together with py-scoop")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.6:", type=("build", "run"))
    depends_on("py-pandas@0.18:", type=("build", "run"))
    depends_on("py-deap@1.3.3:", type=("build", "run"))
    depends_on("py-efel@2.13:", type=("build", "run"))
    depends_on("py-ipyparallel", type=("build", "run"))
    depends_on("py-pickleshare@0.7.3:", type=("build", "run"))
    depends_on("py-jinja2@2.8:", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-pebble@4.6:", type=("build", "run"))
    depends_on("py-scoop@0.7:", type=("build", "run"), when="+scoop")
    depends_on("neuron@7.4:", type=("build", "run"))

    def setup_run_environment(self, env):
        env.unset("PMI_RANK")
        env.set("NEURON_INIT_MPI", "0")
