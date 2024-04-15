# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginSlurmJobstep(PythonPackage):
    """A Snakemake executor plugin for running srun jobs inside of SLURM jobs
    (meant for internal use by snakemake-executor-plugin-slurm)."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-slurm-jobstep"
    pypi = (
        "snakemake_executor_plugin_slurm_jobstep/"
        "snakemake_executor_plugin_slurm_jobstep-0.1.9.tar.gz"
    )

    license("MIT")

    version(
        "0.1.10",
        sha256="ba4a7eea38b409b8e50f357385dca7830d9e4a20494649d6b6257cd5d91b6809",
        url="https://pypi.org/packages/98/79/0156409cbcc1523f0600c7c463c26d5a592f02d86bcab7e953465e65f455/snakemake_executor_plugin_slurm_jobstep-0.1.10-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.11:3", when="@0.1.5:")
        depends_on("py-snakemake-interface-common@1.13:", when="@0.1.5:")
        depends_on("py-snakemake-interface-executor-plugins@8.2:8", when="@0.1.10")
