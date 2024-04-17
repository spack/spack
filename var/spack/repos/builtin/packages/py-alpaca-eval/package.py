# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAlpacaEval(PythonPackage):
    """An automatic evaluator for instruction-following language models.
    Human-validated, high-quality, cheap, and fast."""

    homepage = "https://github.com/tatsu-lab/alpaca_eval"
    pypi = "alpaca_eval/alpaca_eval-0.2.8.tar.gz"

    maintainers("meyersbs")

    license("Apache-2.0")

    version(
        "0.2.8",
        sha256="a83279fcccfb63b81a60a410b4165291a586b7efde8709ac5a1380917530ac4f",
        url="https://pypi.org/packages/c9/35/f7d6eb3909fd36ecbf927186a2c23cd257c45dc95dd1314dc2169a7aa9d9/alpaca_eval-0.2.8-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.10:")
        depends_on("py-datasets")
        depends_on("py-fire")
        depends_on("py-openai", when="@:0.5.1")
        depends_on("py-pandas")
        depends_on("py-python-dotenv", when="@0.2.2:")
        depends_on("py-tiktoken@0.3.2:")
