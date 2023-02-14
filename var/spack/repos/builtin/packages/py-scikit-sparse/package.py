# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScikitSparse(PythonPackage):
    """Sparse matrix tools extending scipy.sparse, but with incompatible licenses"""

    homepage = "https://github.com/scikit-sparse/scikit-sparse"
    pypi = "scikit-sparse/scikit-sparse-0.4.8.tar.gz"
    git = "https://github.com/scikit-sparse/scikit-sparse.git"

    maintainers("cgcgcg")

    version("0.4.8", sha256="2a224c60da3ef951975242ea777478583d3265efc72db5cfb7861686521a4009")

    depends_on("python@3.6:3.11", type=("build", "link", "run"))
    depends_on("py-setuptools@40.8:", type="build")
    depends_on("py-cython@0.22:", type="build")
    depends_on("py-numpy@1.13.3:", type=("build", "link", "run"))
    depends_on("py-scipy@0.19:", type="run")
    depends_on("suite-sparse", type=("build", "link", "run"))

    import_modules = ["sksparse"]
