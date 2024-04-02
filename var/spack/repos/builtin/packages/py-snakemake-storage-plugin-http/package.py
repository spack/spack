# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginHttp(PythonPackage):
    """Snakemake storage plugin for downloading input files from HTTP(s)."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-http"
    pypi = "snakemake_storage_plugin_http/snakemake_storage_plugin_http-0.2.3.tar.gz"

    license("MIT")

    version(
        "0.2.3",
        sha256="04f090a79e0ce61fe3e0871d58306a4d133554ed7a7c5514f58b622afd636a90",
        url="https://pypi.org/packages/1d/7f/0c6de70886eaf9e83076d782ae4d8d86343b792101209c97918f25610297/snakemake_storage_plugin_http-0.2.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.11:3", when="@0.2.2:")
        depends_on("py-requests@2.31:")
        depends_on("py-requests-oauthlib@1.3.1:1")
        depends_on("py-snakemake-interface-common@1.14:", when="@0.2.2:")
        depends_on("py-snakemake-interface-storage-plugins@3:", when="@0.2.2:")
