# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Busybox(Package):
    """BusyBox combines tiny versions of many common UNIX utilities into
    a single small executable. It provides replacements for most of
    the utilities you usually find in GNU fileutils, shellutils, etc"""

    homepage = "https://busybox.net"
    url      = "https://busybox.net/downloads/busybox-1.31.0.tar.bz2"

    version('1.31.1', sha256='d0f940a72f648943c1f2211e0e3117387c31d765137d92bd8284a3fb9752a998')

    def install(self, spec, prefix):
        make('defconfig')
        make()
        make('install')
        install_tree('', prefix)
