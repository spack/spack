# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBotorch(PythonPackage):
    """BoTorch is a library for Bayesian Optimization built on PyTorch."""

    homepage = "https://botorch.org/"
    pypi = "botorch/botorch-0.6.4.tar.gz"

    maintainers("adamjstewart")

    version("0.6.4", sha256="3fd28417f55749501a45378f72cd5ca7614e2e05b7b65c6b4eb9b72378bc665a")

    depends_on("python@3.7:", type=("build", "run"))
    # TODO: replace this after concretizer learns how to concretize separate build deps
    depends_on("py-setuptools", type="build")
    # depends_on('py-setuptools@:47', type='build')
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-torch@1.9:", type=("build", "run"))
    depends_on("py-gpytorch@1.6:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-multipledispatch", type=("build", "run"))
    depends_on("py-pyro-ppl@1.8.0", type=("build", "run"))
