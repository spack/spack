# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBbpWorkflow(PythonPackage):
    """Blue Brain Workflow."""

    homepage = "https://bbpgitlab.epfl.ch/nse/bbp-workflow"
    git = "ssh://git@bbpgitlab.epfl.ch/nse/bbp-workflow.git"

    version("3.1.42", tag="bbp-workflow-v3.1.42")

    depends_on("py-setuptools", type=("build"))

    depends_on("py-requests-unixsocket", type=("build", "run"))
    depends_on("py-dask+diagnostics", type=("build", "run"))
    depends_on("py-distributed", type=("build", "run"))
    depends_on("py-luigi", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-luigi-tools", type=("build", "run"))
    depends_on("py-sh@:1", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-bluepy", type=("build", "run"))
    depends_on("py-bluepy-configfile", type=("build", "run"))
    depends_on("py-bluepysnap", type=("build", "run"))
    depends_on("py-voxcell", type=("build", "run"))
    depends_on("py-entity-management", type=("build", "run"))
    depends_on("py-xarray", type=("build", "run"))
    depends_on("py-pint-xarray", type=("build", "run"))
    depends_on("py-cheetah3", type=("build", "run"))
    depends_on("py-elephant", type=("build", "run"))
    depends_on("py-neo", type=("build", "run"))
    depends_on("py-pyarrow+parquet", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-cwl-luigi", type=("build", "run"))
    depends_on("py-cwl-registry", type=("build", "run"))
    depends_on("py-brayns", type=("build", "run"))
    depends_on("py-bluepyemodel", type=("build", "run"))
    depends_on("py-bluepyemodelnexus", type=("build", "run"))

    # extra deps to include in the module
    # depend on a version with BBP ca root patch
    depends_on("py-certifi@2021.10.8", type=("build", "run"))
    # enable serialization of xarray to zarr compressed array
    depends_on("py-zarr", type=("build", "run"))
    # enable workflow tasks launch jupyter notebooks
    depends_on("py-notebook", type=("build", "run"))
    # enable workflow tasks create ipyparallel cluster
    depends_on("py-ipyparallel", type=("build", "run"))
    # rdflib plugins pull this from python-daemon
    depends_on("py-docutils", type=("build", "run"))

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.spec["py-distributed"].prefix.bin)
        env.prepend_path("PATH", self.spec["py-notebook"].prefix.bin)
        env.prepend_path("PATH", self.spec["py-ipython"].prefix.bin)
        env.prepend_path("PATH", self.spec["py-ipyparallel"].prefix.bin)
        env.prepend_path("PATH", self.spec["py-luigi"].prefix.bin)
