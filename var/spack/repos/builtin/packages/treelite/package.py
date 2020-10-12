# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Treelite(CMakePackage):
    """Treelite is a model compiler for efficient deployment of
    decision tree ensembles."""

    homepage = "https://github.com/dmlc/treelite"
    url      = "https://github.com/dmlc/treelite/archive/0.93.tar.gz"

    version('0.93',    sha256='7d347372f7fdc069904afe93e69ed0bf696ba42d271fe2f8bf6835d2ab2f45d5')

    variant('protobuf', default=True, description='Build with protobuf')

    depends_on('protobuf', when='+protobuf')

    def cmake_args(self):
        args = []

        if '+protobuf' in self.spec:
            args.append('-DENABLE_PROTOBUF:BOOL=ON')
            args.append('-DProtobuf_LIBRARY={0}'.format(self.spec['protobuf'].prefix))
        else:
            args.append('-DENABLE_PROTOBUF:BOOL=OFF')

        return args
