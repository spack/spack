# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginGcs(PythonPackage):
    """A Snakemake storage plugin for Google Cloud Storage."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-gcs"
    pypi = "snakemake_storage_plugin_gcs/snakemake_storage_plugin_gcs-0.1.3.tar.gz"

    license("MIT")

    version(
        "0.1.3",
        sha256="83c7ab8f7bf0f63b43603ec1e6684c4c1442ec7ca79e40fc1e9054ad383acf2d",
        url="https://pypi.org/packages/64/8c/dad6ccb934d1895a55b202ca431d16fbe696051ce4cf144130615dc2eb80/snakemake_storage_plugin_gcs-0.1.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.11:3")
        depends_on("py-google-cloud-storage@2.12:")
        depends_on("py-google-crc32c@1.1.2:", when="@0.1.2:")

    # This is not in the package definition, but I am pretty sure that it is needed
    # https://github.com/snakemake/snakemake-storage-plugin-gcs/issues/19
