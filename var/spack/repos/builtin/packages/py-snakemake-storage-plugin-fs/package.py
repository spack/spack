# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginFs(PythonPackage):
    """A Snakemake storage plugin that reads and writes from a locally mounted filesystem
    using rsync."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-fs"
    pypi = "snakemake_storage_plugin_fs/snakemake_storage_plugin_fs-0.1.5.tar.gz"

    license("MIT")

    version(
        "0.2.0",
        sha256="228fdcf4688993a0e9910d788d35f7a11311d0d5b4d4940ac3c63e16621c1330",
        url="https://pypi.org/packages/9c/3d/e7d3de5b78d898119bfdc59d3988919134a5cd1ff458e89daaebf265d3ab/snakemake_storage_plugin_fs-0.2.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.11:3")
        depends_on("py-reretry@0.11.8:", when="@0.2:")
        depends_on("py-snakemake-interface-common@1.17:", when="@0.2:")
        depends_on("py-snakemake-interface-storage-plugins@3.1:", when="@0.2:")
        depends_on("py-sysrsync@1.1.1:")
