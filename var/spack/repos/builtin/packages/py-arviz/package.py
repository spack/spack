# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArviz(PythonPackage):
    """ArviZ (pronounced "AR-vees") is a Python package for exploratory
    analysis of Bayesian models. Includes functions for posterior analysis,
    model checking, comparison and diagnostics."""

    homepage = "https://github.com/arviz-devs/arviz"
    pypi = "arviz/arviz-0.6.1.tar.gz"

    license("Apache-2.0")

    version(
        "0.6.1",
        sha256="fa613e6f796501f352462c747638d7e1d7ae3e3ed36e665e547def1b2524602c",
        url="https://pypi.org/packages/ec/8b/83472d660e004a69b8e7b3c1dd12a607167774097138445d0dda1a3590dc/arviz-0.6.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-matplotlib@3.0.0:", when="@:0.12")
        depends_on("py-netcdf4", when="@:0.14")
        depends_on("py-numpy@1.12.0:", when="@0.5:0.12")
        depends_on("py-packaging", when="@0.6:")
        depends_on("py-pandas@0.23.0:", when="@0.5:0.12")
        depends_on("py-scipy@0.19:", when="@0.5:0.12")
        depends_on("py-xarray@0.11:", when="@0.5:0.9")
