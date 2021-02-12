# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxres(AutotoolsPackage, XorgPackage):
    """libXRes - X-Resource extension client library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXRes"
    xorg_mirror_path = "lib/libXres-1.0.7.tar.gz"

    version('1.2.0', sha256='5b62feee09f276d74054787df030fceb41034de84174abec6d81c591145e043a')
    version('1.0.7', sha256='488c9fa14b38f794d1f019fe62e6b06514a39f1a7538e55ece8faf22482fefcd')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xextproto')
    depends_on('resourceproto@1.0:')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
