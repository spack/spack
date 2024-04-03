# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOnnxmltools(PythonPackage):
    """Converts Machine Learning models to ONNX"""

    homepage = "https://github.com/onnx/onnxmltools"
    pypi = "onnxmltools/onnxmltools-1.10.0.tar.gz"

    license("Apache-2.0")

    # Source tarball not available on PyPI
    version(
        "1.11.1",
        sha256="c8a108e36cb12b5f1393b03ffba05d3f6be16f421de5666ae9e25bbc3b593594",
        url="https://pypi.org/packages/31/20/6d459df8fc012a2c3f2641c44bccd2bd27b5efa98ad453cf8ecbdb9b8c63/onnxmltools-1.11.1-py3-none-any.whl",
    )
    version(
        "1.11.0",
        sha256="7a7c2c79a25c7d1a56dc008040b5e30f0c550739a2b49cbf645e068844b2a747",
        url="https://pypi.org/packages/d1/e7/40cb0bad3fb837bc8cc0c73b26e3250a175b5352dfadeb77fd8b51d92213/onnxmltools-1.11.0-py2.py3-none-any.whl",
    )
    version(
        "1.10.0",
        sha256="9bede96c469ee02a9e343a2f5196a9db43c1090b78f92ed94fcd8e36e3aae7ec",
        url="https://pypi.org/packages/94/09/a23b3be452455a2d2a551349d7cb350889a014a40a0b432410b48707d8b3/onnxmltools-1.10.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy")
        depends_on("py-onnx")
        depends_on("py-skl2onnx", when="@:1.11")
