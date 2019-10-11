# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Czmq(AutotoolsPackage):
    """ A C interface to the ZMQ library """
    homepage = "http://czmq.zeromq.org"
    url      = "https://github.com/zeromq/czmq/archive/v4.0.2.tar.gz"

    version('4.1.1', 'a2ab03cddd14399c6ba75b030a256211')
    version('4.0.2', 'a65317a3fb8238cf70e3e992e381f9cc')
    version('3.0.2', '23e9885f7ee3ce88d99d0425f52e9be1')

    depends_on('libtool', type='build')
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('pkgconfig', type='build')
    depends_on("libuuid")
    depends_on('zeromq')

    def autoreconf(self, spec, prefix):
        autogen = Executable('./autogen.sh')
        autogen()

    def configure_args(self):
        config_args = []
        if 'clang' in self.compiler.name:
            config_args.append("CFLAGS=-Wno-gnu")
            config_args.append("CXXFLAS=-Wno-gnu")
        return config_args
