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

    version("0.1.5", sha256="f1a54248008b6c65102a1fde2064e3b66aadd9f6795522bacb452deecfe181ad")

    depends_on("py-sysrsync@1.1.1:1", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.14.2:1", type=("build", "run"))
    depends_on("py-snakemake-interface-storage-plugins@3", type=("build", "run"))

    depends_on("python@3.11:", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
