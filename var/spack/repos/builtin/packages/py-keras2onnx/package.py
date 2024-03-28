# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKeras2onnx(PythonPackage):
    """Converts Machine Learning models to ONNX for use in Windows ML"""

    homepage = "https://github.com/onnx/keras-onnx"

    url = "https://github.com/onnx/keras-onnx/archive/refs/tags/v1.7.0.tar.gz"

    license("MIT")

    version(
        "1.7.0",
        sha256="341159ae4b8b2ae06d876e71475e87a364ee2160b49981474a53f1d62b9626e6",
        url="https://pypi.org/packages/a6/2f/c7aef8f8215c62d55ea05f5b36737c1726e4fea6c73970909523ae497fd9/keras2onnx-1.7.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-fire", when="@1.5.2:")
        depends_on("py-numpy")
        depends_on("py-onnx")
        depends_on("py-onnxconverter-common@1.7:", when="@1.7:")
        depends_on("py-protobuf")
        depends_on("py-requests", when="@1.5:")
