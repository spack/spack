# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeExecutorPluginGooglebatch(PythonPackage):
    """A Snakemake executor plugin."""

    homepage = "https://github.com/snakemake/snakemake-executor-plugin-googlebatch"
    pypi = (
        "snakemake_executor_plugin_googlebatch/snakemake_executor_plugin_googlebatch-0.3.0.tar.gz"
    )

    license("MIT")

    version(
        "0.3.0",
        sha256="ba323e2ed9c8f3c45711cd07544a9d11992f5dcbea55822d649bb82bfb074cf4",
        url="https://pypi.org/packages/0e/d5/c65ad6bcaa04a330ea3d8f74f796ef97274633e7e877dc0378fa51d4d902/snakemake_executor_plugin_googlebatch-0.3.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.11:3")
        depends_on("py-google-api-core@2.12.0:2.12.0.0,2.13:")
        depends_on("py-google-cloud-batch@0.17.1:")
        depends_on("py-google-cloud-logging@3.8:")
        depends_on("py-google-cloud-storage@2.12:")
        depends_on("py-jinja2@3.1.2:")
        depends_on("py-requests@2.31:")
        depends_on("py-snakemake-interface-common@1.14:")
        depends_on("py-snakemake-interface-executor-plugins@8.1.1:8", when="@:0.3.0")
