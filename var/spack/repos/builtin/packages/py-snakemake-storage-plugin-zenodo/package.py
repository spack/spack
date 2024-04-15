# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginZenodo(PythonPackage):
    """A Snakemake storage plugin for reading from and writing to zenodo.org."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-zenodo"
    pypi = "snakemake_storage_plugin_zenodo/snakemake_storage_plugin_zenodo-0.1.2.tar.gz"

    license("MIT")

    version(
        "0.1.2",
        sha256="739958562bde0e5cb539e45032621334c95ef791cf05ed711ff737c1dd588b9b",
        url="https://pypi.org/packages/61/60/1f9fc05e55a0df725f0335939b4d1e56e0fb3c09eca01448361f29934aa8/snakemake_storage_plugin_zenodo-0.1.2-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.11:3")
        depends_on("py-requests@2.31:")
        depends_on("py-snakemake-interface-common@1.14.4:")
        depends_on("py-snakemake-interface-storage-plugins@3:", when="@0.1.1:")
