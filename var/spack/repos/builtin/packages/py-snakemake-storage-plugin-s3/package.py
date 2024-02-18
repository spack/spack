# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginS3(PythonPackage):
    """A Snakemake storage plugin for S3 API storage (AWS S3, MinIO, etc.)."""

    pypi = "snakemake_storage_plugin_s3/snakemake_storage_plugin_s3-0.2.9.tar.gz"

    license("MIT")

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-s3"
    version("0.2.9", sha256="41cb23326f37dc576d4a1deac15b3f5a647e26ca957a69ae06b128c044ba2f32")

    depends_on("py-boto3@1.33:1", type=("build", "run"))
    depends_on("py-botocore@1.33:1", type=("build", "run"))
    depends_on("py-urllib3@2:2.1", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.14:1", type=("build", "run"))
    depends_on("py-snakemake-interface-storage-plugins@3", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
