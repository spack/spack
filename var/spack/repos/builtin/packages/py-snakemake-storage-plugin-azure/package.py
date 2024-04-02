# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginAzure(PythonPackage):
    """A Snakemake storage plugin to read and write from Azure Blob Storage."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-azure"
    pypi = "snakemake_storage_plugin_azure/snakemake_storage_plugin_azure-0.1.4.tar.gz"

    license("MIT")

    version(
        "0.1.4",
        sha256="bafb2797c94a92954765ce3816f15d09aa51b566505d51e0fc3d046fb10ef4ec",
        url="https://pypi.org/packages/66/6a/0f696f1d87dea8450c8aed92e1f7c4dd382585c4e699c0a0a002a0d769fd/snakemake_storage_plugin_azure-0.1.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.11:3")
        depends_on("py-azure-core@1.29.5:")
        depends_on("py-azure-identity@1.15.0:")
        depends_on("py-azure-storage-blob@12.19.0:")
        depends_on("py-snakemake-interface-common@1.15:", when="@0.1.4:")
        depends_on("py-snakemake-interface-storage-plugins@3:", when="@0.1.2:")
