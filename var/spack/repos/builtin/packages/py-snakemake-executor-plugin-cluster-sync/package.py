# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginClusterSync(PythonPackage):
    """A Snakemake executor plugin for cluster jobs that are executed synchronously."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-cluster-sync"
    pypi = (
        "snakemake_executor_plugin_cluster_sync/"
        "snakemake_executor_plugin_cluster_sync-0.1.3.tar.gz"
    )

    license("MIT")

    version(
        "0.1.3",
        sha256="4178c6ddd6166c739042447ae40151172258c19307aace4b0683ab3a6efc4c12",
        url="https://pypi.org/packages/2c/dd/83997fd4e7c0c799721328cbdac1c80f97c95172595ec94c54b3cbd09a33/snakemake_executor_plugin_cluster_sync-0.1.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.11:3", when="@0.1.1:")
        depends_on("py-snakemake-interface-common@1.14:", when="@0.1.2:")
        depends_on("py-snakemake-interface-executor-plugins@8.1:8", when="@0.1.2:0.1.3")
