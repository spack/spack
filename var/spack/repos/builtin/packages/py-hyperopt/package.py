# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHyperopt(PythonPackage):
    """Hyperopt is a Python library for serial and parallel optimization over
    awkward search spaces, which may include real-valued, discrete, and
    conditional dimensions."""

    homepage = "https://hyperopt.github.io/hyperopt/"
    pypi = "hyperopt/hyperopt-0.2.5.tar.gz"

    version(
        "0.2.5",
        sha256="dc5c7cceaf33c125b727cf92709e70035d94dd507831dae66406ac762a18a253",
        url="https://pypi.org/packages/a6/07/bd524635d218adae139be320eeac87fb4fbbd45c63b0bd58930c9e91f1fc/hyperopt-0.2.5-py2.py3-none-any.whl",
    )

    variant("atpe", default=False, description="ATPE")
    variant("mongo", default=False, description="MongoTrials")
    variant("spark", default=False, description="SparkTrials")

    with default_args(type="run"):
        depends_on("py-cloudpickle", when="@0.2:")
        depends_on("py-future", when="@0.1.1:")
        depends_on("py-lightgbm", when="@0.2:+atpe")
        depends_on("py-networkx@2.2:", when="@0.2.4:")
        depends_on("py-numpy", when="@0.1.1:")
        depends_on("py-scikit-learn", when="@0.2:+atpe")
        depends_on("py-scipy", when="@0.1.1:")
        depends_on("py-six", when="@0.1.1:")
        depends_on("py-tqdm", when="@0.1.2:")
