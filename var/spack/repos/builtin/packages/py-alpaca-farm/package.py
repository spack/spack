# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAlpacaFarm(PythonPackage):
    """AlpacaFarm is a simulator that enables research and development on learning
    from feedback at a fraction of the usual cost, promoting accessible research on
    instruction following and alignment."""

    homepage = "https://github.com/tatsu-lab/alpaca_farm"
    pypi = "alpaca_farm/alpaca_farm-0.1.9.tar.gz"

    maintainers("meyersbs")

    license("Apache-2.0")

    version(
        "0.1.9",
        sha256="24ba2fa007205a98f8c7208071e54edcf295a03bb2d19b71a1da27d27dafc537",
        url="https://pypi.org/packages/15/40/c7098f4ebe1006e2b6843eebfd05f15431d5312dcc37efa785f4089a78d3/alpaca_farm-0.1.9-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.10:", when="@0.1.6:")
        depends_on("py-accelerate@0.18:", when="@:0.1.9")
        depends_on("py-alpaca-eval@0.2.8:", when="@0.1.9:0.1")
        depends_on("py-datasets")
        depends_on("py-einops")
        depends_on("py-fire")
        depends_on("py-markdown")
        depends_on("py-nltk")
        depends_on("py-openai")
        depends_on("py-pandas")
        depends_on("py-scikit-learn")
        depends_on("py-sentencepiece")
        depends_on("py-statsmodels")
        depends_on("py-tabulate")
        depends_on("py-tiktoken@0.3.2:")
        depends_on("py-torch@1.13.1:")
        depends_on("py-transformers@4.26:", when="@:0.1.9")
        depends_on("py-wandb")
