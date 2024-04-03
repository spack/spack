# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginAzureBatch(PythonPackage):
    """A Snakemake executor plugin for submitting jobs to Microsoft Azure Batch."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-azure-batch"
    pypi = (
        "snakemake_executor_plugin_azure_batch/snakemake_executor_plugin_azure_batch-0.1.3.tar.gz"
    )

    license("MIT")

    version(
        "0.1.3",
        sha256="63d7a459d3f023ee3b16a82afab24be8011ad9760a6a59e56ea7381b6c272e2c",
        url="https://pypi.org/packages/3a/38/77ec61b97d8a5b9984de444a37462f300a8420c0ac0e5133bbbacbad915e/snakemake_executor_plugin_azure_batch-0.1.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.11:3")
        depends_on("py-azure-batch@14:")
        depends_on("py-azure-identity@1.14.0:")
        depends_on("py-azure-mgmt-batch@17:", when="@0.1.3:")
        depends_on("py-azure-storage-blob@12.17.0:")
        depends_on("py-msrest@0.7.1:")
        depends_on("py-snakemake-interface-common@1.15:", when="@0.1.2:")
        depends_on("py-snakemake-interface-executor-plugins@8.1.1:8", when="@0.1.2:")
