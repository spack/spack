# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeInterfaceExecutorPlugins(PythonPackage):
    """This package provides a stable interface for interactions between Snakemake and its
    executor plugins."""

    homepage = "https://github.com/snakemake/snakemake-interface-executor-plugins"
    pypi = "snakemake_interface_executor_plugins/snakemake_interface_executor_plugins-8.2.0.tar.gz"

    license("MIT")

    version(
        "8.2.0",
        sha256="b5d7f83b699492648bd44fc601736f15c86a2aa7ba8e5e011282e83a38b0e05f",
        url="https://pypi.org/packages/48/da/bd3caeb1de705bf3d1ff072b6788ef3189f784990bf027957f835eecf4dc/snakemake_interface_executor_plugins-8.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.11:3")
        depends_on("py-argparse-dataclass@2:")
        depends_on("py-snakemake-interface-common@1.12:")
        depends_on("py-throttler@1.2.2:")
