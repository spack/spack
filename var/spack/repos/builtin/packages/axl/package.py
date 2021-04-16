# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Axl(CMakePackage):
    """Asynchronous transfer library"""

    homepage = "https://github.com/ecp-veloc/AXL"
    url      = "https://github.com/ecp-veloc/AXL/arceive/v0.4.0.tar.gz"
    git      = "https://github.com/ecp-veloc/axl.git"

    tags = ['ecp']

    version('master', branch='master')
    version('0.4.0', sha256='0530142629d77406a00643be32492760c2cf12d1b56c6b6416791c8ff5298db2')
    version('0.3.0', sha256='3f5efff87be700a5792a0ee9a7aeae45c640e2936623b024e8bc1056f7952a46', deprecated=True)
    version('0.2.0', sha256='a0babe3576da30919f89df2f83c76bd01d06345919f2e54d4dddcd6f73faedcc', deprecated=True)
    version('0.1.1', sha256='ebbf231bb542a6c91efb79fce05d4c8a346d5506d88ae1899fb670be52e81933', deprecated=True)

    variant('bbapi_fallback', default='False',
            description='Using BBAPI, if source or destination don\'t support \
            file extents then fallback to pthreads')

    depends_on('kvtree')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('platform=cray'):
            args.append("-DAXL_LINK_STATIC=ON")
        args.append("-DWITH_KVTREE_PREFIX=%s" % self.spec['kvtree'].prefix)

        if '+bbapi_fallback' in self.spec:
            args.append('-DENABLE_BBAPI_FALLBACK=ON')
        else:
            args.append('-DENABLE_BBAPI_FALLBACK=OFF')

        return args
