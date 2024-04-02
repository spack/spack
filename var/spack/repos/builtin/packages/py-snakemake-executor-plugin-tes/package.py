# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginTes(PythonPackage):
    """A Snakemake executor plugin for submitting jobs via GA4GH TES."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-tes"
    pypi = "snakemake_executor_plugin_tes/snakemake_executor_plugin_tes-0.1.2.tar.gz"

    license("MIT")

    version(
        "0.1.2",
        sha256="3757627870a07f6552c3948ddd71823e6aabe24c6b3c827046e64a255d2c8fde",
        url="https://pypi.org/packages/28/03/c19699ee9b0bf84748d37bdab9bb88f575df6f0f2be45bc2433dcd0f5195/snakemake_executor_plugin_tes-0.1.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.11:3")
        depends_on("py-py-tes@0.4.2:0")
        depends_on("py-snakemake-interface-common@1.14:", when="@0.1.1:")
        depends_on("py-snakemake-interface-executor-plugins@8.1.1:8", when="@0.1.2")
