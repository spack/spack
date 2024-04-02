# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginClusterGeneric(PythonPackage):
    """A Snakemake executor plugin for submitting jobs to a cluster."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-cluster-generic"
    pypi = (
        "snakemake_executor_plugin_cluster_generic/"
        "snakemake_executor_plugin_cluster_generic-1.0.7.tar.gz"
    )

    license("MIT")

    version(
        "1.0.7",
        sha256="8ac47d50923d1cadd3e1f847ce2da6b983d7f98a5f6448307665438daa7fad32",
        url="https://pypi.org/packages/c5/53/98856650e6f693edd0fd9d194b353ab660357de638c6f48f185a54ae3ac9/snakemake_executor_plugin_cluster_generic-1.0.7-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.11:3", when="@1.0.4:")
        depends_on("py-snakemake-interface-common@1.13:", when="@1.0.4:")
        depends_on("py-snakemake-interface-executor-plugins@8.1:8", when="@1.0.5:1.0.8")
