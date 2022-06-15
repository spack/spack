# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySkl2onnx(PythonPackage):
    """Convert scikit-learn models to ONNX"""

    homepage = "https://github.com/onnx/sklearn-onnx"
    pypi     = "skl2onnx/skl2onnx-1.10.3.tar.gz"

    version('1.10.3', sha256='798933378145412b9876ab3ff2c1dd5f241a7296406d786262000afa8d329628')

    depends_on('py-setuptools',  type='build')
    depends_on('py-numpy@1.15:', type=('build', 'run'))
    depends_on('py-scipy@1.0:',  type=('build', 'run'))
    depends_on('py-protobuf',    type=('build', 'run'))
    depends_on('py-onnx@1.2.1:', type=('build', 'run'))
    depends_on('py-scikit-learn@0.19:', type=('build', 'run'))
    depends_on('py-onnxconverter-common@1.7.0:', type=('build', 'run'))
