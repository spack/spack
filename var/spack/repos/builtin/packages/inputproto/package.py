# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Inputproto(AutotoolsPackage):
    """X Input Extension.

    This extension defines a protocol to provide additional input devices
    management such as graphic tablets."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/inputproto"
    url      = "https://www.x.org/archive/individual/proto/inputproto-2.3.2.tar.gz"

    version('2.3.2', '6450bad6f8d5ebe354b01b734d1fd7ca')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
