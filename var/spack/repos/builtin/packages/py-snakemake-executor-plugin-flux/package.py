# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginFlux(PythonPackage):
    """A Snakemake executor plugin for the Flux scheduler."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-flux"
    pypi = "snakemake_executor_plugin_flux/snakemake_executor_plugin_flux-0.1.0.tar.gz"

    license("MIT")

    version(
        "0.1.0",
        sha256="e0f02a1be00020bfb625e3d05d5ab584e0f56520d84ba729af957ecf2b9f8469",
        url="https://pypi.org/packages/27/e4/f7cb4276eb8e4e2230326ffeb3b559423c19d3e7480d1e1ad584ba355e34/snakemake_executor_plugin_flux-0.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.11:3")
        depends_on("py-snakemake-interface-common@1.14:")
        depends_on("py-snakemake-interface-executor-plugins@8.1.1:8", when="@:0.1.0")
