# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGlmnetPython(PythonPackage):
    """Python implementation of glmnet, a package that fits a generalized
    linear model via penalized maximum likelihood"""

    homepage = "https://glmnet-python.readthedocs.io/en/latest/glmnet_vignette.html"

    url = "https://github.com/bbalasub1/glmnet_python/archive/refs/tags/1.0.tar.gz"

    version("1.0", sha256="33ee0af8ed3ff4349f6d8275a53b27b9447ba1b5df475369c05d17a85991b2cd")

    depends_on("py-setuptools", type="build")
    depends_on("py-joblib@0.10.3:", type=("build", "run"))
    # https://github.com/bbalasub1/glmnet_python/issues/64
    depends_on("py-scipy@:1.8.1", type=("build", "run"))
