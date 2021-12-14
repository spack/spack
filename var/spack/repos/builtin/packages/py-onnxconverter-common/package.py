# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOnnxconverterCommon(PythonPackage):
    """ONNX Converter and Optimization Tools"""

    homepage = "https://github.com/microsoft/onnxconverter-common"
    url      = "https://github.com/microsoft/onnxconverter-common/archive/refs/tags/v1.9.0.tar.gz"

    version('1.9.0', sha256='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy',      type=('build', 'run'))
    depends_on('py-protobuf',   type=('build', 'run'))
    depends_on('py-onnx',       type=('build', 'run'))
