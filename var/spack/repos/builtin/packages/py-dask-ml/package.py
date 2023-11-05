# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDaskMl(PythonPackage):
    """Scalable Machine Learning with Dask."""

    homepage = "https://ml.dask.org/"
    pypi = "dask-ml/dask-ml-1.8.0.tar.gz"

    version("1.8.0", sha256="8fc4ac3ec1915e382fb8cae9ff1ec9b5ac1bee0b6f4c6975d6e6cb7191a4a815")

    variant("docs", default=False, description="Build HTML documentation")
    variant("xgboost", default=False, description="Deploys XGBoost alongside Dask")

    depends_on("python@3.6:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-dask+array+dataframe@2.4.0:", type=("build", "run"))
    depends_on("py-distributed@2.4.0:", type=("build", "run"))
    depends_on("py-numba", type=("build", "run"))
    depends_on("py-numpy@1.17.3:", type=("build", "run"))
    depends_on("py-pandas@0.24.2:", type=("build", "run"))
    depends_on("py-scikit-learn@0.23:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-dask-glm@0.2.0:", type=("build", "run"))
    depends_on("py-multipledispatch@0.4.9:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))

    depends_on("py-graphviz", when="+docs", type=("build", "run"))
    depends_on("py-heapdict", when="+docs", type=("build", "run"))
    depends_on("py-ipykernel", when="+docs", type=("build", "run"))
    depends_on("py-ipython", when="+docs", type=("build", "run"))
    depends_on("py-nbsphinx", when="+docs", type=("build", "run"))
    depends_on("py-nose", when="+docs", type=("build", "run"))
    depends_on("py-numpydoc", when="+docs", type=("build", "run"))
    depends_on("py-sortedcontainers", when="+docs", type=("build", "run"))
    depends_on("py-sphinx", when="+docs", type=("build", "run"))
    depends_on("py-sphinx-rtd-theme", when="+docs", type=("build", "run"))
    depends_on("py-sphinx-gallery", when="+docs", type=("build", "run"))
    depends_on("py-testpath", when="+docs", type=("build", "run"))
    depends_on("py-tornado", when="+docs", type=("build", "run"))
    depends_on("py-zict", when="+docs", type=("build", "run"))
    depends_on("py-dask-sphinx-theme@1.1.0:", when="+docs", type=("build", "run"))
    depends_on("py-nbsphinx", when="+docs", type=("build", "run"))

    depends_on("py-xgboost+dask", when="+docs", type=("build", "run"))
    depends_on("py-xgboost+dask", when="+xgboost", type=("build", "run"))

    patch("xgboost_dependency.patch")

    conflicts("+docs", when="%gcc target=aarch64:")

    @run_after("install")
    def install_docs(self):
        if "+docs" in self.spec:
            with working_dir("docs"):
                make("html")
            install_tree("docs", self.prefix.docs)
