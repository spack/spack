# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAxPlatform(PythonPackage):
    """Adaptive experimentation is the machine-learning guided process of
    iteratively exploring a (possibly infinite) parameter space in order to identify
    optimal configurations in a resource-efficient manner. Ax currently supports
    Bayesian optimization and bandit optimization as exploration strategies. Bayesian
    optimization in Ax is powered by BoTorch, a modern library for Bayesian
    optimization research built on PyTorch."""

    homepage = "https://github.com/facebook/Ax"
    pypi = "ax-platform/ax-platform-0.3.1.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version(
        "0.3.1",
        sha256="1f9dc8038dd3cf30cf3bd14de49733229a0c1def9a39d740cfd9e4020adf95be",
        url="https://pypi.org/packages/b8/2e/7aa462e763ab81a515f7d5cea67c691c3403b96ef5f500a47deeb311a8d7/ax_platform-0.3.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.2.7:0.3.3")
        depends_on("py-botorch@0.8.3", when="@0.3.1")
        depends_on("py-ipywidgets", when="@0.3:")
        depends_on("py-jinja2")
        depends_on("py-pandas")
        depends_on("py-plotly@5.12:", when="@0.3:")
        depends_on("py-scikit-learn")
        depends_on("py-scipy")
        depends_on("py-typeguard@2.13.3:2", when="@0.3.1:0.3.5")
