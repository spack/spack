# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-pytorch-toolkit-cu-11-8
#
# You can edit this file again by typing:
#
#     spack edit py-pytorch-toolkit-cu-11-8
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyPytorchToolkitCu118(PythonPackage):
    """Python package used to dev neural networks using Pytorch==2.0.1 and CUDA==11.8"""
    homepage = "https://pytorch.org"
    url = "https://download.pytorch.org/whl/torch-cuda80/torch_cuda80-0.1.6.post20-cp35-cp35m-linux_x86_64.whl"

    maintainers("borin98")
    version("0.1.6.post20", sha256="a266c8bbc3c883f42888bdd85b6fd21da2a6941fb270db554caad409cca3b89c", expand=False)

    depends_on("python@3.8:3.11", type=("build", "run"))