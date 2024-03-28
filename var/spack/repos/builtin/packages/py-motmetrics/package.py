# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMotmetrics(PythonPackage):
    """The py-motmetrics library provides a Python implementation of
    metrics for benchmarking multiple object trackers (MOT)."""

    homepage = "https://github.com/cheind/py-motmetrics"
    pypi = "motmetrics/motmetrics-1.2.0.tar.gz"

    license("MIT")

    version(
        "1.2.0",
        sha256="78be33a951fe17b4a1b2c17b235b769920b700345b83e46d4b436f3efaf54d9f",
        url="https://pypi.org/packages/9c/28/9c3bc8e2a87f4c9e7b04ab72856ec7f9895a66681a65973ffaf9562ef879/motmetrics-1.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-flake8", when="@1.2:1.2.0")
        depends_on("py-flake8-import-order", when="@1.2:1.2.0")
        depends_on("py-numpy@1.12.1:", when="@:1.0,1.1.1:")
        depends_on("py-pandas@0.23.1:", when="@1.1.3:")
        depends_on("py-pytest", when="@1.2:1.2.0")
        depends_on("py-pytest-benchmark", when="@1.2:1.2.0")
        depends_on("py-scipy@0.19:", when="@:1.0,1.1.1:")
        depends_on("py-xmltodict@0.12:", when="@1.2:")
