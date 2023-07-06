# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLinearOperator(PythonPackage):
    """A linear operator implementation, primarily designed for finite-dimensional
    positive definite operators (i.e. kernel matrices)."""

    homepage = "https://github.com/cornellius-gp/linear_operator/"
    pypi = "linear_operator/linear_operator-0.1.1.tar.gz"

    maintainers("meyersbs")

    version("0.4.0", sha256="7c57c9f8f258c9785c0db4dd7625f4dd03a340313d7314cba0b633644909f5c6")
    version("0.3.0", sha256="84bf572631a7e1576de6920d81600ca0fedcf6bda2f29dbaf440d6e72ce6abab")
    version("0.1.1", sha256="81adc1aea9e98f3c4f07f5608eb77b689bc61793e9beebfea82155e9237bf1be")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-torch@1.11:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
