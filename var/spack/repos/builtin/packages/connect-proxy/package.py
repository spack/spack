# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ConnectProxy(MakefilePackage):
    """`connect.c` is a simple relaying command to make network connection
    via SOCKS and https proxy"""

    homepage = "https://bitbucket.org/gotoh/connect"
    url      = "https://bitbucket.org/gotoh/connect/get/1.105.tar.bz2"

    version('1.105', '0e5581651ce31a78ae87bdffb086c3ad')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('connect', prefix.bin)
