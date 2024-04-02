# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyModin(PythonPackage):
    """Modin: Make your pandas code run faster by changing one line of code."""

    homepage = "https://github.com/modin-project/modin"
    pypi = "modin/modin-0.16.2.tar.gz"

    license("Apache-2.0")

    version(
        "0.16.2",
        sha256="6c00c42887d7aac72dcaa1dad4f34f66f22364b4d9df88fde260bf3551d1bb82",
        url="https://pypi.org/packages/d4/d1/0f7de03512702c42133a54a4c0a04a8aa0e2eecd318959c45eb798f8a8f1/modin-0.16.2-py3-none-any.whl",
    )

    variant(
        "engine",
        default="ray",
        values=["ray", "dask", "python", "native"],
        description="Default distribution engine. All engines are installed and "
        "functional as long as dependencies are found at run-time",
    )

    with default_args(type="run"):
        depends_on("py-fsspec", when="@:0.23.0")
        depends_on("py-numpy@1.18.5:", when="@:0.23.0")
        depends_on("py-packaging", when="@:0.23.0")
        depends_on("py-pandas@1.5.1", when="@0.16.2:0.17.0")
        depends_on("py-psutil", when="@0.15.2:0.23.0")

    def setup_run_environment(self, env):
        # modin/config/envvars.py
        env.set("MODIN_ENGINE", self.spec.variants["engine"].value)
