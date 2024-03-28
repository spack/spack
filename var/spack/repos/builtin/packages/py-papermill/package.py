# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPapermill(PythonPackage):
    """Parametrize and run Jupyter and nteract Notebooks."""

    homepage = "https://github.com/nteract/papermill"
    pypi = "papermill/papermill-2.4.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.4.0",
        sha256="baa76f0441257d9a25b3ad7c895e761341b94f9a70ca98cf419247fc728932d9",
        url="https://pypi.org/packages/a2/e2/2f02a7aa739b4a03d20032d2f711e9eb0fd52202debd6df54518eab4403e/papermill-2.4.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-ansiwrap", when="@0.8.8:0.13.2,0.13.4:2.4.0")
        depends_on("py-azure-datalake-store@0.0.30:", when="@0.15:0.17")
        depends_on("py-boto3", when="@0.8:0.13.2,0.13.4:0.17")
        depends_on("py-click", when="@0.4:0.13.2,0.13.4:")
        depends_on("py-entrypoints", when="@0.16.2:")
        depends_on("py-ipython@5.0.0:", when="@0.13.2,0.13.4:1.0")
        depends_on("py-nbclient@0.2:", when="@2.1:")
        depends_on("py-nbformat@5.1.2:", when="@2.3.1:")
        depends_on("py-pyyaml", when="@0.4:0.13.2,0.13.4:")
        depends_on("py-requests", when="@0.11:0.13.2,0.13.4:")
        depends_on("py-tenacity", when="@0.19.1:2.4.0")
        depends_on("py-tqdm@4.32.2:", when="@1.1:")
