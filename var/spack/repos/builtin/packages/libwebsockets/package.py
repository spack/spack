# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libwebsockets(CMakePackage):
    """C library for lightweight websocket clients and servers."""

    homepage = "https://github.com/warmcat/libwebsockets"
    url      = "https://github.com/warmcat/libwebsockets/archive/v2.1.0.tar.gz"
    maintainers = ['ax3l']

    version('2.2.1', '1f641cde2ab3687db3d553f68fe0f620')
    version('2.1.1', '674684ffb90d4a0bcf7a075eb7b90192')
    version('2.1.0', '4df3be57dee43aeebd54a3ed56568f50')
    version('2.0.3', 'a025156d606d90579e65d53ccd062a94')
    version('1.7.9', '7b3692ead5ae00fd0e1d56c080170f07')

    depends_on('zlib')
    depends_on('openssl')
