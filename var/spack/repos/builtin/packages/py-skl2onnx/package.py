# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySkl2onnx(PythonPackage):
    """Convert scikit-learn models to ONNX"""

    homepage = "https://github.com/onnx/sklearn-onnx"
    pypi = "skl2onnx/skl2onnx-1.10.3.tar.gz"

    license("Apache-2.0")

    version(
        "1.12",
        sha256="2b91a1c5051f50a96634189b46fb4184729f858b6dfeda30231e6eea48be99e3",
        url="https://pypi.org/packages/d3/57/62e51efc91606aa447a1aaa54dc31b5028afd564ff7a750f1efc90b582cd/skl2onnx-1.12-py2.py3-none-any.whl",
    )
    version(
        "1.10.3",
        sha256="908bccb2974b6ef852878b28a2a5e65cfe59c7572ea285aee46c64a4b6d2728a",
        url="https://pypi.org/packages/86/2d/055c27bdbcfe8fca11ba901e9161349f608c70173632f8241914d56ed20f/skl2onnx-1.10.3-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy@1.15.0:", when="@1.7:1.13")
        depends_on("py-onnx@1.2:", when="@1.7:")
        depends_on("py-onnxconverter-common@1.7:", when="@1.9.3:")
        depends_on("py-protobuf", when="@1.7:1.13")
        depends_on("py-scikit-learn@0.19.0:", when="@1.7:1.13,1.15:")
        depends_on("py-scipy@1.0.0:", when="@1.7:1.13")

    # Although this dep is undocumented, it's imported at run-time.
