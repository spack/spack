# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBioblend(PythonPackage):
    """BioBlend is a Python library for interacting with the Galaxy API."""

    homepage = "https://bioblend.readthedocs.io"
    pypi = "bioblend/bioblend-1.0.0.tar.gz"

    license("MIT")

    version(
        "1.0.0",
        sha256="db9616a77c614f3de900796079e9db72af739809232702d5ea4acf5ef49b4d38",
        url="https://pypi.org/packages/97/cb/eb052cb733e6422599786f56f5f6bf2a055e7041a522ec3541beb9ee4518/bioblend-1.0.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.17:")
        depends_on("py-requests@2.20:", when="@0.12:")
        depends_on("py-requests-toolbelt@0.5.1:0.8,0.9.1:", when="@0.13:")
        depends_on("py-tuspy", when="@0.18:")
        depends_on("py-typing-extensions", when="@1:")
