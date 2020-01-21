# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class TensorflowServingClient(CMakePackage):
    """A prebuilt tensorflow serving client from the tensorflow serving
       proto files"""

    homepage = "https://github.com/figroc/tensorflow-serving-client"
    url      = "https://github.com/figroc/tensorflow-serving-client/archive/v2.0.0.tar.gz"

    version('2.0.0', sha256='55310ad484f257173ad5194df7f7116b2049260c3d29049ef8d789d1d8bd9948')

    depends_on('protobuf')
    depends_on('grpc')
