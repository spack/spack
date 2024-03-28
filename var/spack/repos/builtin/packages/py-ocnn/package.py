# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOcnn(PythonPackage):
    """O-CNN is an octree-based sparse convolutional neural network
    framework for 3D deep learning."""

    homepage = "https://github.com/octree-nn/ocnn-pytorch"
    pypi = "ocnn/ocnn-2.2.0.tar.gz"

    maintainers("wdconinc")

    license("MIT")

    version(
        "2.2.0",
        sha256="790d689ff5d1b9d26dc6fabe4b1fc72ade8fd71b55f0497dcf7d23595a42aa49",
        url="https://pypi.org/packages/b6/4c/e22fd40215216d5c3d8388e9827392a2daf0462f719800972c3eed2bd5ae/ocnn-2.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy")
        depends_on("py-torch")
