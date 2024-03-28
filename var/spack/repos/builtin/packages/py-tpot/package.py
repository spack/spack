# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTpot(PythonPackage):
    """
    A Python Automated Machine Learning tool that optimizes machine learning
    pipelines using genetic programming.
    """

    homepage = "https://epistasislab.github.io/tpot/"
    pypi = "tpot/TPOT-0.11.5.tar.gz"

    license("LGPL-3.0-only")

    version(
        "0.11.7",
        sha256="6f323bf60bb0bd48992118e1ee5268aa71924a6c4339252494902dac95b64cae",
        url="https://pypi.org/packages/b2/55/a7185198f554ea19758e5ac4641f100c94cba4585e738e2e48e3c40a0b7f/TPOT-0.11.7-py3-none-any.whl",
    )
    version(
        "0.11.5",
        sha256="d2858f314b39deec090b389f1b3acc8b9a89c7a1b284f55da3e42221f64c7a3e",
        url="https://pypi.org/packages/14/5e/cb87b0257033a7a396e533a634079ee151a239d180efe2a8b1d2e3584d23/TPOT-0.11.5-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-deap@1.2:", when="@0.11.1:")
        depends_on("py-joblib@0.13.2:", when="@0.11.1:")
        depends_on("py-numpy@1.16.3:", when="@0.11.1:")
        depends_on("py-pandas@0.24.2:", when="@0.11.1:")
        depends_on("py-scikit-learn@0.22:", when="@0.11.1:0.12.1")
        depends_on("py-scipy@1.3.1:", when="@0.11.1:")
        depends_on("py-stopit@1.1.1:", when="@0.10,0.11.1:")
        depends_on("py-tqdm@4.36.1:", when="@0.11.1:")
        depends_on("py-update-checker@0.16:", when="@0.10,0.11.1:")
        depends_on("py-xgboost@1.1.0:", when="@0.11.6.post3:")
