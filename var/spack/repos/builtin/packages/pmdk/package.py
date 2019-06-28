# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import spack.architecture


class Pmdk(Package):
    """The Persistent Memory Development Kit (PMDK), formerly known as NVML,
    is a library for using memory-mapped persistence, optimized specifically
    for persistent memory
    """

    homepage = "http://pmem.io/pmdk/"
    url      = "https://github.com/pmem/pmdk/archive/1.5.tar.gz"
    git      = "https://github.com/pmem/pmdk.git"

    version('develop', branch='master')
    version('1.6',     sha256='3b99e6c30709326a94d2e73a9247a8dfb58d0a394c5b7714e5c3d8a3ad2e2e9f')
    version('1.5',     sha256='6b069d7207febeb62440e89245e8b18fcdf40b6170d2ec2ef33c252ed16db2d4')

    depends_on('ncurses', when='@1.6:')
    # documentation requires doxygen and a bunch of other dependencies
    patch('0001-make-doc-building-explicit.patch')

    def install(self, spec, prefix):
        make_args = [
            'prefix=%s' % prefix,
            'NDCTL_ENABLE=n',
            'EXTRA_CFLAGS=-Wno-error',
            'BUILD_RPMEM=n',
        ]

        # pmdk is particular about the ARCH specification, must be
        # exactly "x86_64" for build to work
        if 'x86_64' in spack.architecture.sys_type():
            make_args += ['ARCH=x86_64']

        make("install", *make_args)
