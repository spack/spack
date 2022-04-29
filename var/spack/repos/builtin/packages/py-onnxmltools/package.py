# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyOnnxmltools(PythonPackage):
    """Converts Machine Learning models to ONNX"""

    homepage = "https://github.com/onnx/onnxmltools"
    pypi     = "onnxmltools/onnxmltools-1.10.0.tar.gz"

    version('1.10.0', sha256='4eb4605f18ed66553fc17438ac8cf5406d66dcc624bedd76d8067e1b08e6c75d')

    depends_on('py-setuptools',   type='build')
    depends_on('py-numpy',        type=('build', 'run'))
    depends_on('py-onnx',         type=('build', 'run'))
    depends_on('py-skl2onnx',     type=('build', 'run'))
    depends_on('py-onnx-runtime', type=('build', 'run'))
