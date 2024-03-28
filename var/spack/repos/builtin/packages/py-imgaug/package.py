# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImgaug(PythonPackage):
    """A library for image augmentation in machine learning experiments,
    particularly convolutional neural networks. Supports the augmentation of
    images, keypoints/landmarks, bounding boxes, heatmaps and segmentation maps
    in a variety of different ways."""

    homepage = "https://github.com/aleju/imgaug"
    pypi = "imgaug/imgaug-0.3.0.tar.gz"

    license("MIT")

    version(
        "0.4.0",
        sha256="ce61e65b4eb7405fc62c1b0a79d2fa92fd47f763aaecb65152d29243592111f9",
        url="https://pypi.org/packages/66/b1/af3142c4a85cba6da9f4ebb5ff4e21e2616309552caca5e8acefe9840622/imgaug-0.4.0-py2.py3-none-any.whl",
    )
    version(
        "0.3.0",
        sha256="99b8a38e137a76dd2780c4e86fa799ec4d0753cfc9088f9b51789f4a23fbe9d9",
        url="https://pypi.org/packages/11/df/5a3bba95b4600d5ca7aff072082ef0d9837056dd28cc4e738e7ce88dd8f8/imgaug-0.3.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-imageio", when="@0.2.7:")
        depends_on("py-matplotlib", when="@0.2.7:")
        depends_on("py-numpy@1.15.0:", when="@0.2.8:")
        depends_on("py-opencv-python", when="@0.2.8:0.2,0.4:")
        depends_on("py-opencv-python-headless", when="@0.3")
        depends_on("py-pillow", when="@0.2.7:")
        depends_on("py-scikit-image@0.14.2:", when="@0.3:")
        depends_on("py-scipy", when="@0.2.7:")
        depends_on("py-shapely", when="@0.2.7:")
        depends_on("py-six", when="@0.2.7:")
