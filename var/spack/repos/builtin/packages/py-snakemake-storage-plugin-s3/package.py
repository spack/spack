# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginS3(PythonPackage):
    """A Snakemake storage plugin for S3 API storage (AWS S3, MinIO, etc.)."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-s3"
    pypi = "snakemake_storage_plugin_s3/snakemake_storage_plugin_s3-0.2.9.tar.gz"

    license("MIT")

    version(
        "0.2.10",
        sha256="8604e73694470e93d5736baae809dc17359292aced58894df370edaaf2231ece",
        url="https://pypi.org/packages/54/4f/5fc5b99425ed7af30d556a4d2e2c71b799cff49b3b1971da4b5fc05bccae/snakemake_storage_plugin_s3-0.2.10-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.11:3", when="@0.2.3:")
        depends_on("py-boto3@1.33:", when="@0.2.9:")
        depends_on("py-botocore@1.33:", when="@0.2.9:")
        depends_on("py-snakemake-interface-common@1.14:", when="@0.2.8:")
        depends_on("py-snakemake-interface-storage-plugins@3:", when="@0.2.7:")
        depends_on("py-urllib3@2.0.0:2.1", when="@0.2.10:")
