# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Onnx(CMakePackage):
    """Open Neural Network Exchange (ONNX).

    ONNX provides an open source format for AI models, both deep learning and
    traditional ML. It defines an extensible computation graph model, as well
    as definitions of built-in operators and standard data types."""

    homepage = "https://github.com/onnx/onnx"
    url      = "https://github.com/onnx/onnx/archive/refs/tags/v1.9.0.tar.gz"

    version('1.9.0', sha256='61d459a5f30604cabec352574119a6685dfd43bfa757cfbff52be9471d5b8ea0')

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')
    depends_on('python', type='build')
    depends_on('protobuf')

    generator = 'Ninja'
