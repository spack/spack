# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginKubernetes(PythonPackage):
    """A Snakemake executor plugin for submission of jobs to Kubernetes."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-kubernetes"
    pypi = "snakemake_executor_plugin_kubernetes/snakemake_executor_plugin_kubernetes-0.1.4.tar.gz"

    license("MIT")

    version(
        "0.1.4",
        sha256="17f3b75579d02a44fa4f578fee0e41c03c2eacc2d0c91ecbe2971fdf06ef86cf",
        url="https://pypi.org/packages/39/b3/7744cae5393b7b0f679678116c4bb1c3a6e070943409adc79de6b3f810cd/snakemake_executor_plugin_kubernetes-0.1.4-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.11:3")
        depends_on("py-kubernetes@27.2.0:27", when="@:0.1.4")
        depends_on("py-snakemake-interface-common@1.14.1:", when="@0.1.2:")
        depends_on("py-snakemake-interface-executor-plugins@8.0.2:8", when="@0.1.3:0.1.4")
