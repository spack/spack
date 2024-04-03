# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBotorch(PythonPackage):
    """BoTorch is a library for Bayesian Optimization built on PyTorch."""

    homepage = "https://botorch.org/"
    pypi = "botorch/botorch-0.6.4.tar.gz"

    maintainers("adamjstewart", "meyersbs")

    license("MIT")

    version(
        "0.8.4",
        sha256="a3370e1778d6922036df7abb4cffdfd367f206413bf0a5510b8287e157435ad6",
        url="https://pypi.org/packages/ac/13/e9eddd3b5b335f924e35417e7552cceeb88b75155c2f7d206ad2b3110e2a/botorch-0.8.4-py3-none-any.whl",
    )
    version(
        "0.8.3",
        sha256="69cee323902a63281f0edc01f1ce0e67159eed53372ab96943daf14b03345a35",
        url="https://pypi.org/packages/f7/e0/785ad78406bfa9b41accdc09862a289e591072cd7cfbeacf5b7ae6dc1ef7/botorch-0.8.3-py3-none-any.whl",
    )
    version(
        "0.6.4",
        sha256="818fa6353534d4e48765ecd5028a651ca1e453688e3bdfd1e5eaae1818e1940f",
        url="https://pypi.org/packages/b4/43/d6ac02db7a812ad9c9ab02ca94b4046cff4e1bca4ee88d3191c0ba38f0db/botorch-0.6.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.7:0.8")
        depends_on("python@3.7:", when="@:0.6")
        depends_on("py-gpytorch@1.10", when="@0.8.4:0.8")
        depends_on("py-gpytorch@1.9.1:1.9", when="@0.8.1:0.8.3")
        depends_on("py-gpytorch@1.6:", when="@0.6:0.6.4")
        depends_on("py-linear-operator@0.4", when="@0.8.4:0.8")
        depends_on("py-linear-operator@0.3", when="@0.8.1:0.8.3")
        depends_on("py-multipledispatch", when="@0.6.1:")
        depends_on("py-pyro-ppl@1.8.4:", when="@0.8.1:")
        depends_on("py-pyro-ppl@1.8:1.8.0", when="@0.6.3:0.6.4")
        depends_on("py-scipy")
        depends_on("py-torch@1.12:", when="@0.8.2:0.8")
        depends_on("py-torch@1.9:", when="@0.6:0.6.4")
