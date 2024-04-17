# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXhistogram(PythonPackage):
    """Fast, flexible, label-aware histograms for numpy and xarray."""

    homepage = "https://github.com/xgcm/xhistogram"
    pypi = "xhistogram/xhistogram-0.3.2.tar.gz"

    license("MIT")

    version(
        "0.3.2",
        sha256="ad55330d55296d273b3370678223fde0f50085e04cb744c7b3b0bb7702a2c6bf",
        url="https://pypi.org/packages/18/08/1432dd10193a5d45294bd42042a5631259ee5a12cd2e9075350546d07a03/xhistogram-0.3.2-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.2:")
        depends_on("py-dask@2.3:+array", when="@0.3.2:")
        depends_on("py-numpy@1.17.0:", when="@0.3:")
        depends_on("py-xarray@0.12:")
