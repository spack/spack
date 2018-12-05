# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Clfft(CMakePackage):
    """a software library containing FFT functions written in OpenCL"""

    homepage = "https://github.com/clMathLibraries/clFFT"
    url      = "https://github.com/clMathLibraries/clFFT/archive/v2.12.2.tar.gz"

    version('2.12.2', '9104d85f9f2f3c58dd8efc0e4b06496f')

    variant('client', default=True,
            description='build client and callback client')

    depends_on('opencl@1.2:')
    depends_on('boost@1.33.0:', when='+client')

    root_cmakelists_dir = 'src'

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DBUILD_CLIENT:BOOL={0}'.format((
                'ON' if '+client' in spec else 'OFF')),
            '-DBUILD_CALLBACK_CLIENT:BOOL={0}'.format((
                'ON' if '+client' in spec else 'OFF'))
        ]
        return args
