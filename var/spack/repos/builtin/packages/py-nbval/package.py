# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNbval(PythonPackage):
    """Py.test plugin for validating Jupyter notebooks.

    The plugin adds functionality to py.test to recognise and collect Jupyter notebooks.
    The intended purpose of the tests is to determine whether execution of the stored
    inputs match the stored outputs of the .ipynb file. Whilst also ensuring that the
    notebooks are running without errors.
    """

    homepage = "https://github.com/computationalmodelling/nbval"
    pypi = "nbval/nbval-0.9.6.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.9.6",
        sha256="4f9b780997d8942408853513f2c5ee6c1863de193559fc3f95e1c1cde8110439",
        url="https://pypi.org/packages/b0/92/23d60d4593b6e69f2114caf6fec238ce461233a8633dcbef6f619ad339c9/nbval-0.9.6-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-coverage", when="@0.9:0.9.3,0.9.5:")
        depends_on("py-ipykernel")
        depends_on("py-jupyter-client")
        depends_on("py-nbformat")
        depends_on("py-pytest@2.8:", when="@:0.10")
        depends_on("py-six", when="@:0.9")
