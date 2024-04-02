# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeInterfaceReportPlugins(PythonPackage):
    """The interface for Snakemake report plugins."""

    homepage = "https://github.com/snakemake/snakemake-interface-report-plugins"
    pypi = "snakemake_interface_report_plugins/snakemake_interface_report_plugins-1.0.0.tar.gz"

    license("MIT")

    version(
        "1.0.0",
        sha256="e39cf2f27a36bda788dd97ede8fd056f887e00dca2d14ffea91dbc696d1f17cd",
        url="https://pypi.org/packages/5e/8d/aa3e3eab25854b358862b319e1c703ecd96d287ba93fe9ee6708f5074850/snakemake_interface_report_plugins-1.0.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.11:3")
        depends_on("py-snakemake-interface-common@1.16:")
