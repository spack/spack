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

    version("0.1.10", sha256="321b6bdf7883a8fb40ff4aeeb88633502e4db8394e40b6628db41a430c2eae2b")

    depends_on("py-snakemake-interface-common@1.13:1", type=("build", "run"))
    depends_on("py-snakemake-interface-executor-plugins@8.2:8", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
