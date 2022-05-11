# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package_defs import *


class PyOnnx(PythonPackage):
    """Open Neural Network Exchange (ONNX) is an open ecosystem that
       empowers AI developers to choose the right tools as their
       project evolves. ONNX provides an open source format for AI
       models, both deep learning and traditional ML. It defines an
       extensible computation graph model, as well as definitions of
       built-in operators and standard data types. Currently we focus
       on the capabilities needed for inferencing (scoring)."""

    homepage = "https://github.com/onnx/onnx"
    pypi = "Onnx/onnx-1.6.0.tar.gz"

    version('1.8.1', sha256='9d65c52009a90499f8c25fdfe5acda3ac88efe0788eb1d5f2575a989277145fb')
    version('1.6.0', sha256='3b88c3fe521151651a0403c4d131cb2e0311bd28b753ef692020a432a81ce345')
    version('1.5.0', sha256='1a584a4ef62a6db178c257fffb06a9d8e61b41c0a80bfd8bcd8a253d72c4b0b4')

    depends_on('py-setuptools', type='build')
    # Protobuf version limit is due to https://github.com/protocolbuffers/protobuf/pull/8794
    depends_on('protobuf@:3.17')
    depends_on('py-protobuf+cpp@:3.17', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-numpy@1.16.6:', type=('build', 'run'), when='@1.8.1:')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-typing@3.6.4:', when='^python@:3.4', type=('build', 'run'))
    depends_on('py-typing-extensions@3.6.2.1:', type=('build', 'run'))
    depends_on('cmake@3.1:', type='build')
    depends_on('py-pytest-runner', type='build')

    # 'python_out' does not recognize dllexport_decl.
    patch('remove_dllexport_decl.patch', when='@:1.6.0')
