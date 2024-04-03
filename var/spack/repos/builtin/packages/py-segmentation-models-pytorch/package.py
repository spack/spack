# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySegmentationModelsPytorch(PythonPackage):
    """Python library with Neural Networks for Image Segmentation based on PyTorch."""

    homepage = "https://github.com/qubvel/segmentation_models.pytorch"
    pypi = "segmentation_models_pytorch/segmentation_models_pytorch-0.2.0.tar.gz"

    license("MIT")

    version(
        "0.3.3",
        sha256="b4317d6f72cb1caf4b7e1d384096970e202600275f54deb8e774fc04d6c8b82e",
        url="https://pypi.org/packages/cb/70/4aac1b240b399b108ce58029ae54bc14497e1bbc275dfab8fd3c84c1e35d/segmentation_models_pytorch-0.3.3-py3-none-any.whl",
    )
    version(
        "0.3.2",
        sha256="dba48e7ead5d34fcb6e5c6d04d6d7c5a61a53fa84264e5481df788a22a1bd66b",
        url="https://pypi.org/packages/40/7d/6a91c9608fd54c115e617e233c44b7023dc4445d478b258d04314afbd02a/segmentation_models_pytorch-0.3.2-py3-none-any.whl",
    )
    version(
        "0.3.1",
        sha256="02c261825aba831e849ec28481321294cc9796acf004c53bdf1844d594fb71e1",
        url="https://pypi.org/packages/18/31/8211a419a327ba506cc398a68e02e6fa3bf0275161c5f82339f13fbc4009/segmentation_models_pytorch-0.3.1-py3-none-any.whl",
    )
    version(
        "0.3.0",
        sha256="753fb1b301a294bf014d846f320f2b714af03cc90b31bfbcdd88819652de3806",
        url="https://pypi.org/packages/98/d3/7bd25846310d7dad6bd30f9ffc7eea3f354c95cdf7bc5421937a9d40c6ee/segmentation_models_pytorch-0.3.0-py3-none-any.whl",
    )
    version(
        "0.2.1",
        sha256="98822571470867fb0f416c112c32f7f1d21702dd32195ec8f7736932c2de0486",
        url="https://pypi.org/packages/f2/4d/839cd59ce604e3fae72d1d0d45928accf92fa4a3f6f07dc70d1d78f5db65/segmentation_models_pytorch-0.2.1-py3-none-any.whl",
    )
    version(
        "0.2.0",
        sha256="d5528719a03c343d20cdaf6ede40160d66ae9fdd14280e5ce47240de46f76992",
        url="https://pypi.org/packages/63/62/f0c1614f07df58317c85c3203adcfdf2249b505c2f05990f5e0af872a5c4/segmentation_models_pytorch-0.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.3.2:")
        depends_on("py-efficientnet-pytorch@0.7.1:", when="@0.3:")
        depends_on("py-efficientnet-pytorch@0.6.3:0.6", when="@0.1.2:0.2")
        depends_on("py-pillow", when="@0.3:")
        depends_on("py-pretrainedmodels@0.7.4:", when="@:0.0.1,0.0.3:")
        depends_on("py-timm@0.9.2", when="@0.3.3:")
        depends_on("py-timm@0.6.12", when="@0.3.2")
        depends_on("py-timm@0.4.12:0.4", when="@0.2:0.3.1")
        depends_on("py-torchvision@0.5:", when="@0.2:")
        depends_on("py-tqdm", when="@0.3:")
