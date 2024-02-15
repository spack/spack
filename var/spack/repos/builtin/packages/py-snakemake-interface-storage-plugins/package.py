# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeInterfaceStoragePlugins(PythonPackage):
    """This package provides a stable interface for interactions between Snakemake and its storage
    plugins."""

    homepage = "https://github.com/snakemake/snakemake-interface-storage-plugins"
    pypi = "snakemake_interface_storage_plugins/snakemake_interface_storage_plugins-3.0.0.tar.gz"

    license("MIT")

    version("3.0.0", sha256="f20d85ee7e86a1e2ffa3f72e2385dd5abb17fa7b58a26cba8ba59096872fe169")

    depends_on("py-wrapt@1.15:1", type=("build", "run"))
    depends_on("py-reretry@0.11.8:0.11", type=("build", "run"))
    depends_on("py-throttler@1.2.2:1", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.12:1", type=("build", "run"))

    depends_on("python@3.11:", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
