# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pmdk(Package):
    """The Persistent Memory Development Kit (PMDK), formerly known as NVML,
    is a library for using memory-mapped persistence, optimized specifically
    for persistent memory
    """

    homepage = "http://pmem.io/pmdk/"
    url      = "https://github.com/pmem/pmdk/archive/1.5.tar.gz"
    git      = "https://github.com/pmem/pmdk.git"

    version('develop', branch='master')
    version('1.8',     sha256='a241ea76ef76d233cb92826b6823ed48091a2fb6963282a4fea848dbce68aa21')
    version('1.7', sha256='865ce1b422bc83109cb4a63dcff8fd1077eea3617e668faf6a043208d8be03ca')
    version('1.6',     sha256='3b99e6c30709326a94d2e73a9247a8dfb58d0a394c5b7714e5c3d8a3ad2e2e9f')
    version('1.5',     sha256='6b069d7207febeb62440e89245e8b18fcdf40b6170d2ec2ef33c252ed16db2d4')

    depends_on('ncurses', when='@1.6:')
    # documentation requires doxygen and a bunch of other dependencies
    patch('0001-make-doc-building-explicit.patch', when="@:1.7")
    patch('pmem-1.8-disable-docs.patch', when='@1.8')

    def install(self, spec, prefix):
        make_args = [
            'prefix=%s' % prefix,
            'NDCTL_ENABLE=n',
            'EXTRA_CFLAGS=-Wno-error',
            'BUILD_RPMEM=n',
        ]

        # pmdk prior to 1.8 was particular about the ARCH specification, must
        # be exactly "x86_64" for build to work
        if spec.target.family == 'x86_64':
            make_args += ['ARCH=x86_64']

        make("install", *make_args)
