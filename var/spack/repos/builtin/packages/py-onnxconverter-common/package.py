# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOnnxconverterCommon(PythonPackage):
    """ONNX Converter and Optimization Tools"""

    homepage = "https://github.com/microsoft/onnxconverter-common"
    pypi     = "onnxconverter-common/onnxconverter-common-1.9.0.tar.gz"

    version('1.9.0', sha256='8e129c3602d1ef7619c5f3d34a53005b997137ea769362f1f8dd1ddab57ed216')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy',      type=('build', 'run'))
    depends_on('py-protobuf',   type=('build', 'run'))
    depends_on('py-onnx',       type=('build', 'run'))

