# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libffs(CMakePackage):
    """FFS is a middleware library for data communication,
    including representation, processing and marshaling
    that preserves the performance of traditional approaches
    while relaxing the requirement of a priori knowledge
    and providing complex run-time flexibility.
    """

    homepage = "http://www.cc.gatech.edu/systems/projects/FFS"
    url      = "https://github.com/GTkorvo/ffs/archive/v1.1.tar.gz"
    git      = "https://github.com/GTkorvo/ffs.git"

    version('develop', branch='master')
    version('1.5',   'c41c5f5f448b627740deecd695b7bbf8')
    version('1.1.1', 'aa1c8ad5cf35e8cf76735e3a60891509')
    version('1.1',   '561c6b3abc53e12b3c01192e8ef2ffbc')

    depends_on('flex', type='build', when='@:1.4')
    depends_on('bison', type='build', when='@:1.4')
    depends_on('gtkorvo-cercs-env', type='build', when='@:1.4')
    depends_on('gtkorvo-atl')
    depends_on('gtkorvo-dill')

    def cmake_args(self):
        args = ["-DTARGET_CNL=1"]
        if self.spec.satisfies('@1.5:'):
            args.append("-DBUILD_SHARED_LIBS=OFF")
        else:
            args.append("-DENABLE_BUILD_STATIC=STATIC")

        if self.run_tests:
            args.append('-DENABLE_TESTING=0')
        else:
            args.append('-DENABLE_TESTING=0')

        return args
