# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginFtp(PythonPackage):
    """A Snakemake plugin for handling input and output via FTP."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-ftp"
    pypi = "snakemake_storage_plugin_ftp/snakemake_storage_plugin_ftp-0.1.2.tar.gz"

    license("MIT")

    version(
        "0.1.2",
        sha256="8331a571f709b9e9729e4d8188c373e371b401e3afcdc2ff25c0da766b98d1ec",
        url="https://pypi.org/packages/9b/73/4acb25f5381a18bfa5a7cf3e4535028ef4f15d9a9e6eb6415fa66e35b8bd/snakemake_storage_plugin_ftp-0.1.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.11:3")
        depends_on("py-ftputil@5.0.4:")
        depends_on("py-snakemake-interface-common@1.15.1:", when="@0.1.2:")
        depends_on("py-snakemake-interface-storage-plugins@3:")
