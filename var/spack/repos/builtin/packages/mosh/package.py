# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mosh(AutotoolsPackage):
    """Remote terminal application that allows roaming, supports intermittent
    connectivity, and provides intelligent local echo and line editing of user
    keystrokes. Mosh is a replacement for SSH. It's more robust and responsive,
    especially over Wi-Fi, cellular, and long-distance links.
    """

    homepage = "https://mosh.org/"
    url      = "https://mosh.org/mosh-1.2.6.tar.gz"

    version('1.3.2', '5122f4d2b973ab7c38dcdac8c35cb61e')
    version('1.3.0', 'd961276995936953bf2d5a794068b076')
    version('1.2.6', 'bb4e24795bb135a754558176a981ee9e')

    depends_on('protobuf')
    depends_on('ncurses')
    depends_on('zlib')
    depends_on('openssl')

    depends_on('pkgconfig', type='build')
    depends_on('perl', type='run')

    build_directory = 'spack-build'
