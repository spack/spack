# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginSlurm(PythonPackage):
    """A Snakemake executor plugin for submitting jobs to a SLURM cluster."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-slurm"
    pypi = "snakemake_executor_plugin_slurm/snakemake_executor_plugin_slurm-0.3.0.tar.gz"

    license("MIT")

    version("0.3.1", sha256="3c45605515f73020d437872e6003de661ddd17a09e2e60780b2d19a5668f0eb5")

    depends_on("py-throttler@1.2.2:1", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.13:1", type=("build", "run"))
    depends_on("py-snakemake-interface-executor-plugins@8.2:8", type=("build", "run"))
    depends_on("py-snakemake-executor-plugin-slurm-jobstep@0.1.10:0.1", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
