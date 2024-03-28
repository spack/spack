# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyChartStudio(PythonPackage):
    """Utilities for interfacing with plotly's Chart Studio."""

    homepage = "https://pypi.org/project/chart-studio/"
    pypi = "chart-studio/chart-studio-1.1.0.tar.gz"

    license("MIT")

    version(
        "1.1.0",
        sha256="fd183185d6e6d31c642567145c1a862f941ca9c7695aac8b2f3ebbcbcea31a7a",
        url="https://pypi.org/packages/ca/ce/330794a6b6ca4b9182c38fc69dd2a9cbff60fd49421cb8648ee5fee352dc/chart_studio-1.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-plotly", when="@:1.0.0-alpha1,1.0.0-alpha3:")
        depends_on("py-requests", when="@:1.0.0-alpha1,1.0.0-alpha3:")
        depends_on("py-retrying@1.3.3:", when="@:1.0.0-alpha1,1.0.0-alpha3:")
        depends_on("py-six", when="@:1.0.0-alpha1,1.0.0-alpha3:")
