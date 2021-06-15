# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xnnpack(CMakePackage):
    """High-efficiency floating-point neural network inference operators for
    mobile, server, and Web"""

    homepage = "https://github.com/google/XNNPACK"
    git      = "https://github.com/google/XNNPACK.git"

    version('master', branch='master')
    version('2021-02-22', commit='55d53a4e7079d38e90acd75dd9e4f9e781d2da35')  # py-torch@1.8:1.9
    version('2020-03-23', commit='1b354636b5942826547055252f3b359b54acff95')  # py-torch@1.6:1.7
    version('2020-02-24', commit='7493bfb9d412e59529bcbced6a902d44cfa8ea1c')  # py-torch@1.5

    depends_on('cmake@3.5:', type='build')
    depends_on('ninja', type='build')
    depends_on('fp16')
    depends_on('cpuinfo')  # provides CLog
    depends_on('pthreadpool')

    generator = 'Ninja'

    def cmake_args(self):
        return [self.define('XNNPACK_USE_SYSTEM_LIBS', True)]
