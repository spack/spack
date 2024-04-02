# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImbalancedLearn(PythonPackage):
    """imbalanced-learn is a python package offering a number of re-sampling
    techniques commonly used in datasets showing strong between-class imbalance.
    It is compatible with scikit-learn and is part of scikit-learn-contrib
    projects."""

    homepage = "https://github.com/scikit-learn-contrib/imbalanced-learn"
    pypi = "imbalanced-learn/imbalanced-learn-0.10.1.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version(
        "0.10.1",
        sha256="7b630516696c09b2b5a5398df8db19d73db0c13fa065d2f1407a6d2037794bc6",
        url="https://pypi.org/packages/11/80/911e581a4fc973179e3a48c1272435aa09cce21c12af122c3886d3d35cb5/imbalanced_learn-0.10.1-py3-none-any.whl",
    )

    variant("optional", default=False, description="Enable optional dependencies.")

    with default_args(type="run"):
        depends_on("py-joblib@1.1.1:", when="@0.10:")
        depends_on("py-keras@2.4.3:", when="@0.9:+optional")
        depends_on("py-numpy@1.17.3:", when="@0.9.1:")
        depends_on("py-pandas@1.0.5:", when="@0.9.1:+optional")
        depends_on("py-scikit-learn@1.0.2:", when="@0.10:")
        depends_on("py-scipy@1.3.2:", when="@0.9.1:0.10")
        depends_on("py-tensorflow@2.4.3:", when="@0.9:+optional")
        depends_on("py-threadpoolctl@2:", when="@0.9:")

    # From setup.py:

    # From https://imbalanced-learn.org/stable/install.html#getting-started:
