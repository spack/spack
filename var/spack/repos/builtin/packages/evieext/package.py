# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Evieext(AutotoolsPackage):
    """Extended Visual Information Extension (XEVIE).

    This extension defines a protocol for a client to determine information
    about core X visuals beyond what the core protocol provides."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/evieproto"
    url      = "https://www.x.org/archive/individual/proto/evieext-1.1.1.tar.gz"

    version('1.1.1', '018a7d24d0c7926d594246320bcb6a86')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
