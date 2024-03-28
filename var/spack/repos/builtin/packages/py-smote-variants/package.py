# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySmoteVariants(PythonPackage):
    """Variants of the synthetic minority oversampling technique (SMOTE) for
    imbalanced learning"""

    homepage = "https://github.com/analyticalmindsltd/smote_variants"
    pypi = "smote_variants/smote_variants-0.7.3.tar.gz"

    version(
        "0.7.3",
        sha256="51425df3ae21f941f050def8363c02ead350941a74c0f17d072a7108c254b95c",
        url="https://pypi.org/packages/ee/94/9e7a507de0628dc8b9eedc38535472d0a086cbda86d2e85d126f9dd889a1/smote_variants-0.7.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-joblib", when="@0.1.1:")
        depends_on("py-keras", when="@0.1.5:")
        depends_on("py-metric-learn", when="@0.5:")
        depends_on("py-minisom")
        depends_on("py-mkl", when="@0.3.10:")
        depends_on("py-numpy", when="@:0.1.2,0.7.3:")
        depends_on("py-pandas", when="@:0.1.2,0.2.6:")
        depends_on("py-scikit-learn", when="@0.2.1:")
        depends_on("py-scipy", when="@:0.1.2,0.2.1:")
        depends_on("py-seaborn", when="@0.6:")
        depends_on("py-statistics")
        depends_on("py-tensorflow", when="@0.1.5:")

    # Not including statistics, because is only needed for python 2
