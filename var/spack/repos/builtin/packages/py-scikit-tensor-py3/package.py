# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScikitTensorPy3(PythonPackage):
    """A python module for multilinear algebra and tensor factorizations."""

    homepage = "http://github.com/evertrol/scikit-tensor-py3"
    pypi = "scikit-tensor-py3/scikit-tensor-py3-0.4.1.tar.gz"

    maintainers("meyersbs")

    version("0.4.1", sha256="b45de97ebd57e0213f54e891bf9a0549957eb2387f4df9f3dc3f7a50f8818b0a")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.16:1.16", type=("build", "run"))
    depends_on("py-scipy@1.3:1.3", type=("build", "run"))
