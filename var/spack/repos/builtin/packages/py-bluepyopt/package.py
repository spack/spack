# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyBluepyopt(PythonPackage):
    """Bluebrain Python Optimisation Library"""

    homepage = "https://github.com/BlueBrain/BluePyOpt"
    pypi = "bluepyopt/bluepyopt-1.9.27.tar.gz"

    license("LGPL-3.0-only")

    # NOTE : while adding new release check pmi_rank.patch compatibility
    version(
        "1.14.4",
        sha256="11de74999036d3d6dd8a003dd0eb073c6325f7feb8c0a38c5f19267275ff424c",
        url="https://pypi.org/packages/5e/45/3494c5c3f9abd414b66f3b4ef93545464b22bbf8c3e81c2896ef5e6899dc/bluepyopt-1.14.4-py3-none-any.whl",
    )

    variant("scoop", default=False)

    with default_args(type="run"):
        depends_on("py-deap@1.3.3:", when="@:0.0,1.12.63:")
        depends_on("py-efel@2.13:", when="@:0.0,1.12.7:")
        depends_on("py-future", when="@:0.0,1.12.7:1.14.4")
        depends_on("py-ipyparallel", when="@:0.0,1.12.7:")
        depends_on("py-jinja2@2.8:", when="@:0.0,1.12.7:")
        depends_on("py-numpy@1.6:", when="@:0.0,1.12.7:")
        depends_on("py-pandas@0.18:", when="@:0.0,1.12.7:")
        depends_on("py-pebble@4.6:", when="@1.14.1:")
        depends_on("py-pickleshare@0.7.3:", when="@:0.0,1.12.7:")
        depends_on("py-scoop", when="@:0.0,1.12.7:+scoop")

    # patch required to avoid hpe-mpi linked mechanism library
    patch("pmi_rank.patch")

    def setup_run_environment(self, env):
        env.unset("PMI_RANK")
        env.set("NEURON_INIT_MPI", "0")
