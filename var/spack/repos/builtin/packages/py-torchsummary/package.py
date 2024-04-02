# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTorchsummary(PythonPackage):
    """Keras has a neat API to view the visualization of the model
    which is very helpful while debugging your network. Here is a
    barebone code to try and mimic the same in PyTorch. The aim is to
    provide information complementary to, what is not provided by
    print(your_model) in PyTorch."""

    homepage = "https://github.com/sksq96/pytorch-summary"
    pypi = "torchsummary/torchsummary-1.5.1.tar.gz"

    version(
        "1.5.1",
        sha256="10f41d1743fb918f83293f13183f532ab1bb8f6639a1b89e5f8592ec1919a976",
        url="https://pypi.org/packages/7d/18/1474d06f721b86e6a9b9d7392ad68bed711a02f3b61ac43f13c719db50a6/torchsummary-1.5.1-py3-none-any.whl",
    )
