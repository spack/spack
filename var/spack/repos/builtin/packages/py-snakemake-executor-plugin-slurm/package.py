# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginSlurm(PythonPackage):
    """A Snakemake executor plugin for submitting jobs to a SLURM cluster."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-slurm"
    pypi = "snakemake_executor_plugin_slurm/snakemake_executor_plugin_slurm-0.3.1.tar.gz"

    license("MIT")

    version(
        "0.3.2",
        sha256="9829dabbd60d98ade8ef5ce0aab069f20ac9df081410a7cec754fc5393272ca0",
        url="https://pypi.org/packages/16/2f/244353069fc209c42473979d74af9f051839a866b1da74c11c28729a78c2/snakemake_executor_plugin_slurm-0.3.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.11:3")
        depends_on("py-snakemake-executor-plugin-slurm-jobstep@0.1.10:", when="@0.2.1:")
        depends_on("py-snakemake-interface-common@1.13:")
        depends_on("py-snakemake-interface-executor-plugins@8.2:8", when="@0.2.1:0.4.1")
        depends_on("py-throttler@1.2.2:")
