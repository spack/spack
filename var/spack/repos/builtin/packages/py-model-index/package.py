# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyModelIndex(PythonPackage):
    """Create a source of truth for ML model results and browse it on Papers with Code"""

    homepage = "https://github.com/paperswithcode/model-index"
    git = "https://github.com/paperswithcode/model-index.git"

    license("MIT")

    version(
        "0.1.11",
        sha256="a2a4d4431cd44e571d31e223cc4b0432663a62689de453bdb666e56a514b0e07",
        url="https://pypi.org/packages/0f/a6/4d4cbbef704f186d143e2859296a610a355992e4eae71582bd598093b36a/model_index-0.1.11-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-click")
        depends_on("py-markdown")
        depends_on("py-ordered-set")
        depends_on("py-pyyaml")
