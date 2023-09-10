# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPytorchToolkitCu118(PythonPackage):
    """Python package used to dev neural networks using Pytorch==2.0.1 and CUDA==11.8"""

    homepage = "https://pytorch.org"
    url = "https://download.pytorch.org/whl/torch-cuda80/torch_cuda80-0.1.6.post20-cp35-cp35m-linux_x86_64.whl"

    maintainers("borin98")
    version(
        "0.1.6.post20", sha256="a266c8bbc3c883f42888bdd85b6fd21da2a6941fb270db554caad409cca3b89c"
    )

    # setup.py
    depends_on("python@3.8:3.11", type=("build", "run"))
    depends_on("py-setuptools", type="build")
