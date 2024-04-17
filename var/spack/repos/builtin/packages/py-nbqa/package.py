# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNbqa(PythonPackage):
    """Run any standard Python code quality tool on a Jupyter Notebook."""

    homepage = "https://github.com/nbQA-dev/nbQA"
    pypi = "nbqa/nbqa-1.6.3.tar.gz"

    license("MIT")

    version(
        "1.6.3",
        sha256="f3bac3e6d322b0a9bf2143d5fea8e5c2f7ac7daced717b3407f2e3279f58afbf",
        url="https://pypi.org/packages/79/d4/ba0bd9e0c51509e29fa6d5a215ddcb8cd60026416f88fa807f500508f7a3/nbqa-1.6.3-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@1.6:")
        depends_on("py-ipython@7.8:")
        depends_on("py-tokenize-rt@3.2:")
        depends_on("py-tomli")
