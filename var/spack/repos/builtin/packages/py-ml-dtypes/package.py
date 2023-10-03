# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMlDtypes(PythonPackage):
    """A stand-alone implementation of several NumPy dtype extensions
    used in machine learning libraries."""

    homepage = "https://github.com/jax-ml/ml_dtypes"
    pypi = "ml_dtypes/ml_dtypes-0.3.1.tar.gz"

    version("0.3.1", sha256="60778f99194b4c4f36ba42da200b35ef851ce4d4af698aaf70f5b91fe70fc611")

    depends_on("python@3.9:", type=("build", "link", "run"))
    depends_on("py-numpy@1.21:", type=("build", "link", "run"))
    # Build dependencies are overconstrained, older versions work just fine
    depends_on("py-pybind11", type=("build", "link"))
    depends_on("py-setuptools", type="build")
