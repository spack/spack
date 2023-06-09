# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGlmnetPython(PythonPackage):
    """Python implementation of glmnet, a package that fits a generalized
    linear model via penalized maximum likelihood"""

    homepage = "https://glmnet-python.readthedocs.io/en/latest/glmnet_vignette.html"

    # This is a fork of the bbalasub1/glmnet_python repo. The docs frequently
    # reference the original, but conda downloads this source instead as it
    # fixes an issue with out-of-date scipy functions
    url = "https://github.com/johnlees/glmnet_python/archive/refs/tags/v1.0.2.tar.gz"

    version("1.0.2", sha256="7a5550514140dabbd27ad4eb1c04db64199d9bb89541e088d9bb162570205e76")

    depends_on("py-setuptools", type="build")
    depends_on("py-joblib@0.10.3:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
