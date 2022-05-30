# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class MongoCxxDriver(CMakePackage):
    """C++ Driver for MongoDB"""

    homepage = "http://www.mongocxx.org"
    url      = "https://github.com/mongodb/mongo-cxx-driver/archive/r3.2.0.tar.gz"

    version('3.6.7', sha256='a9244d3117d4029a2f039dece242eef10e34502e4600e2afa968ab53589e6de7')
    version('3.2.0', sha256='e26edd44cf20bd6be91907403b6d63a065ce95df4c61565770147a46716aad8c')

    depends_on('mongo-c-driver@1.9.2:')
