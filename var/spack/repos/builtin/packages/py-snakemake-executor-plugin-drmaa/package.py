# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginDrmaa(PythonPackage):
    """A snakemake executor plugin for submission of jobs via DRMAA."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-drmaa"
    pypi = "snakemake_executor_plugin_drmaa/snakemake_executor_plugin_drmaa-0.1.3.tar.gz"

    license("MIT")

    version(
        "0.1.3",
        sha256="1f9ee37e0f9ffb2f38f5f08ba5045ac3ae9f60d580f9e6ef2c4faa9fa6a9b665",
        url="https://pypi.org/packages/b1/4a/f7374471e5efd5123ab9084897b23f09063025f7edadf0ac688aaa9d4fb4/snakemake_executor_plugin_drmaa-0.1.3-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.11:3", when="@0.1.1:")
        depends_on("py-drmaa@0.7.9:")
        depends_on("py-snakemake-interface-common@1.13:", when="@0.1.1:")
        depends_on("py-snakemake-interface-executor-plugins@8.1:8", when="@0.1.2:0.1.3")
