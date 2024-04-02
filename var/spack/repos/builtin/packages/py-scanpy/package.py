# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScanpy(PythonPackage):
    """Scanpy is a scalable toolkit for analyzing single-cell
    gene expression data built jointly with anndata."""

    homepage = "https://scanpy.readthedocs.io/en/stable/"
    pypi = "scanpy/scanpy-1.9.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.9.1",
        sha256="9fca3597aef176034ebc3438be3bf859db5c47441e36481d7f9272bd4cd51d2a",
        url="https://pypi.org/packages/51/87/a55c7992cba9b189de70eae37e9f1e2abe6fdaf3f087d30356f28698948e/scanpy-1.9.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1.8:1.9.3")
        depends_on("py-anndata@0.7.4:", when="@1.7:1.9")
        depends_on("py-h5py@3.0.0:", when="@1.9")
        depends_on("py-importlib-metadata@0.7:", when="@:1.9.3 ^python@:3.7")
        depends_on("py-joblib")
        depends_on("py-matplotlib@3.4.0:", when="@1.9.1:1.9.6")
        depends_on("py-natsort")
        depends_on("py-networkx@2.3:", when="@:1.9")
        depends_on("py-numba@0.41:", when="@:1.9")
        depends_on("py-numpy@1.17.0:", when="@:1.9")
        depends_on("py-packaging", when="@:1.9")
        depends_on("py-pandas@1.0.0:", when="@1.9.1:1.9.5")
        depends_on("py-patsy")
        depends_on("py-scikit-learn@0.22:", when="@1.8:1.9.3")
        depends_on("py-scipy@1.4.0:", when="@:1.9")
        depends_on("py-seaborn", when="@:1.9.5")
        depends_on("py-session-info", when="@1.9:")
        depends_on("py-statsmodels@0.10:", when="@:1.9")
        depends_on("py-tqdm")
        depends_on("py-umap-learn@0.3.10:", when="@:1.6.0,1.7.0:1.9")
