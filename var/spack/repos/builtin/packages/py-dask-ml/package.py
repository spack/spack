# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDaskMl(PythonPackage):
    """Scalable Machine Learning with Dask."""

    homepage = "https://ml.dask.org/"
    pypi = "dask-ml/dask-ml-1.8.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.8.0",
        sha256="7b3aa890f348465a5306a4f1e48491698c189af879fd1cf91e0f2adac1129118",
        url="https://pypi.org/packages/06/97/cd1090baa8fcde28b0dda61a1fed2fa695dc2c2bb92b47bd5bce5d95f1c0/dask_ml-1.8.0-py3-none-any.whl",
    )

    variant("docs", default=False)
    variant("xgboost", default=False)

    with default_args(type="run"):
        depends_on("py-dask@2.4:+array+dataframe", when="@1.2,1.5:")
        depends_on("py-dask-glm@0.2:", when="@1.1:1.2,1.5:")
        depends_on("py-dask-xgboost", when="@0.9,0.11:1.2,1.5:+xgboost")
        depends_on("py-distributed@2.4:", when="@1.2,1.5:")
        depends_on("py-multipledispatch@0.4.9:", when="@0.9,0.11:1.2,1.5:")
        depends_on("py-nbsphinx", when="@0.9,0.11:1.2,1.5:+docs")
        depends_on("py-numba", when="@0.9,0.11:1.2,1.5:1.8")
        depends_on("py-numpy@1.17.3:", when="@1.2,1.5:1,2021.10")
        depends_on("py-numpydoc", when="@0.9,0.11:1.2,1.5:+docs")
        depends_on("py-packaging", when="@0.9,0.11:1.2,1.5:")
        depends_on("py-pandas@0.24.2:", when="@1.7:")
        depends_on("py-scikit-learn@0.23.0:", when="@1.5:1")
        depends_on("py-scipy", when="@0.9,0.11:1.2,1.5:")
        depends_on("py-sphinx", when="@0.9,0.11:1.2,1.5:+docs")
        depends_on("py-sphinx-gallery", when="@0.9,0.11:1.2,1.5:+docs")
        depends_on("py-sphinx-rtd-theme", when="@0.9,0.11:1.2,1.5:+docs")
        depends_on("py-xgboost", when="@0.9,0.11:1.2,1.5:+xgboost")

    patch("xgboost_dependency.patch")

    conflicts("+docs", when="%gcc target=aarch64:")

    @run_after("install")
    def install_docs(self):
        if "+docs" in self.spec:
            with working_dir("docs"):
                make("html")
            install_tree("docs", self.prefix.docs)
