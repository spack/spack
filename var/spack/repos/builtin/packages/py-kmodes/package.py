# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKmodes(PythonPackage):
    """Python implementations of the k-modes and k-prototypes clustering
    algorithms for clustering categorical data."""

    homepage = "https://github.com/nicodv/kmodes"
    pypi = "kmodes/kmodes-0.10.1.tar.gz"

    license("MIT")

    version(
        "0.10.1",
        sha256="bce1108382bffc09902c2fe5e1acb1cbb10736634efce2af88f195b4998f7c5e",
        url="https://pypi.org/packages/79/c0/f7d8a0eb41ac6f302b4bc100f91b6e0f2558425ccfefaa0ec0430f77ee97/kmodes-0.10.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-joblib@0.11:", when="@0.10.1:")
        depends_on("py-numpy@1.10.4:", when="@0.2:0.6,0.8:")
        depends_on("py-scikit-learn@0.19.0:", when="@0.10.1:0.10")
        depends_on("py-scipy@0.13.3:", when="@0.8:")
