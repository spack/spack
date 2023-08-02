# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFairscale(PythonPackage):
    """FairScale is a PyTorch extension library for high performance and large
    scale training. This library extends basic PyTorch capabilities while adding
    new SOTA scaling techniques."""

    homepage = "https://github.com/facebookresearch/fairscale"

    url = "https://github.com/facebookresearch/fairscale/archive/refs/tags/v0.4.13.zip"

    version("0.4.13", sha256="a6012a6f23eb0e80dc209dfea992336b4d0d8a191a9080cb746a2b78e5b76cd1")
    version("0.4.4", sha256="b4f9a9ad82e562a1d19ad9249238d135395bc8f4068d292f639308951efff5a8")

    variant(
        "dev-tools", default=False, description="support for cuda.list.gpu, mypy, scaler, weight"
    )

    # from setup.py
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("ninja", type="build")
    # from pyproject.toml
    depends_on("py-wheel@0.30.0:", type="build")
    depends_on("py-setuptools@40.6.2:", type="build")
    # from requirements.txt
    depends_on("py-torch@1.8.0:", type=("build", "run"))
    depends_on("py-numpy@1.22.0:", type=("build", "run"))
    # from requirements-dev.txt
    with when("+dev-tools"):
        depends_on("py-pynvml@8.0.4", type=("build", "run"))
        depends_on("py-numpy@1.22.0:", type=("build", "run"))
        depends_on("py-scikit-learn@1.1.3", type=("build", "run"))
        depends_on("py-pygit2@1.11.1", type=("build", "run"))
        depends_on("py-pgzip@0.3.1", type=("build", "run"))
