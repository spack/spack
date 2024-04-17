# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXskillscore(PythonPackage):
    """Metrics for verifying forecasts."""

    homepage = "https://github.com/xarray-contrib/xskillscore"
    pypi = "xskillscore/xskillscore-0.0.24.tar.gz"

    license("Apache-2.0")

    version(
        "0.0.24",
        sha256="39c3ffa75e2cbbde87470ad957d667e729025ac6a6077ca8efce0ca5f69bfafa",
        url="https://pypi.org/packages/29/6a/3a977c2fc6e57201cda9c85fd5ee1ee72712ea046f884f566f958e38239a/xskillscore-0.0.24-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.0.19:0.0.24")
        depends_on("py-bottleneck", when="@:0.0.24")
        depends_on("py-cftime", when="@0.0.16:0.0.24")
        depends_on("py-dask", when="@:0.0.18,0.0.20:0.0.24")
        depends_on("py-numba@0.52.0:", when="@0.0.19:0.0.24")
        depends_on("py-numpy", when="@0.0.17:")
        depends_on("py-properscoring")
        depends_on("py-scikit-learn", when="@:0.0.24")
        depends_on("py-scipy")
        depends_on("py-toolz", when="@0.0.19:0.0.24")
        depends_on("py-xarray@0.16.1:", when="@0.0.18:")
        depends_on("py-xhistogram@0.3:", when="@0.0.22:")
