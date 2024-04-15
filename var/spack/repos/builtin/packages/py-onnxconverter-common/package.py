# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOnnxconverterCommon(PythonPackage):
    """ONNX Converter and Optimization Tools"""

    homepage = "https://github.com/microsoft/onnxconverter-common"
    url = "https://github.com/microsoft/onnxconverter-common/archive/refs/tags/v1.9.0.tar.gz"

    license("MIT")

    version(
        "1.9.0",
        sha256="02b58ca3351fba4eddf8503e1421cfecd4ddcf2074aea4d58e3b2410e6f67ce5",
        url="https://pypi.org/packages/cc/51/de4e3d84282a6649f4fb73c29b33d96ac1b5e6d30217ed0fff74cc404467/onnxconverter_common-1.9.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-numpy", when="@:1.7,1.8.1:")
        depends_on("py-onnx", when="@:1.7,1.8.1:")
        depends_on("py-protobuf", when="@:1.7,1.8.1:1.13")
