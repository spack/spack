# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libuv(AutotoolsPackage):
    """Multi-platform library with a focus on asynchronous IO"""
    homepage = "http://libuv.org"
    url      = "https://github.com/libuv/libuv/archive/v1.9.0.tar.gz"

    version('1.25.0', sha256='ce3036d444c3fb4f9a9e2994bec1f4fa07872b01456998b422ce918fdc55c254')
    version('1.10.0', sha256='50f4ed57d65af4ab634e2cbdd90c49213020e15b4d77d3631feb633cbba9239f')
    version('1.9.0',  sha256='f8b8272a0d80138b709d38fad2baf771899eed61e7f9578d17898b07a1a2a5eb')

    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')

    # Tries to build an Objective-C file with GCC's C frontend
    # https://github.com/libuv/libuv/issues/2805
    conflicts('%gcc platform=darwin',
              msg='libuv does not compile with GCC on macOS yet, use clang. '
                  'See: https://github.com/libuv/libuv/issues/2805')

    def autoreconf(self, spec, prefix):
        # This is needed because autogen.sh generates on-the-fly
        # an m4 macro needed during configuration
        bash = which("bash")
        bash('autogen.sh')
