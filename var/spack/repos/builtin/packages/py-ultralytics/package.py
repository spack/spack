# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUltralytics(PythonPackage):
    """Ultralytics YOLOv8, developed by Ultralytics, is a cutting-edge, state-of-the-art
    (SOTA) model that builds upon the success of previous YOLO versions and introduces new
    features and improvements to further boost performance and flexibility. YOLOv8 is
    designed to be fast, accurate, and easy to use, making it an excellent choice for a
    wide range of object detection, image segmentation and image classification tasks."""

    homepage = "https://github.com/ultralytics/ultralytics"
    pypi = "ultralytics/ultralytics-8.0.50.tar.gz"

    license("AGPL-3.0")

    version(
        "8.0.50",
        sha256="60c409292cab97ba9893cf7a60a0b2a385f82c7a7f007206a53c0075737dda57",
        url="https://pypi.org/packages/07/d0/97e48941aa91f5c87f576e4268e190d585d011a5a0afd54171522d1bc37f/ultralytics-8.0.50-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3.11.0", when="@8.0.7:8.0.34")
        depends_on("py-certifi@2022.12:", when="@8.0.47:8.0.50")
        depends_on("py-matplotlib@3.2.2:", when="@8:8.0.128,8.0.130:8.0.180")
        depends_on("py-numpy@1.18.5:", when="@:0.0.1,8:8.0.53")
        depends_on("py-opencv-python@4.6:", when="@8.0.17:8.0.128,8.0.130:")
        depends_on("py-pandas@1.1.4:", when="@8:8.0.128,8.0.130:")
        depends_on("py-pillow@7.1.2:", when="@8:8.0.128,8.0.130:")
        depends_on("py-psutil", when="@0.0.5:8.0.128,8.0.130:")
        depends_on("py-pyyaml@5.3.1:", when="@0.0.2:8.0.128,8.0.130:")
        depends_on("py-requests@2.23:", when="@8:8.0.128,8.0.130:")
        depends_on("py-scipy@1.4.1:", when="@8:8.0.128,8.0.130:")
        depends_on("py-seaborn@0.11.0:", when="@8:8.0.128,8.0.130:")
        depends_on("py-sentry-sdk", when="@8.0.8:8.0.109")
        depends_on("py-tensorboard@2.4.1:", when="@8:8.0.50")
        depends_on("py-thop@0.1.1:", when="@8:8.0.103,8.0.190:")
        depends_on("py-torch@1.7:", when="@0.0.4:8.0.128,8.0.130:8.0.151")
        depends_on("py-torchvision@0.8.1:", when="@0.0.4:8.0.128,8.0.130:8.0.151")
        depends_on("py-tqdm@4.64:", when="@8:8.0.128,8.0.130:")
