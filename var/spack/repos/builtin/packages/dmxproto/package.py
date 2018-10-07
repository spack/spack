# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dmxproto(AutotoolsPackage):
    """Distributed Multihead X (DMX) Extension.

    This extension defines a protocol for clients to access a front-end proxy
    X server that controls multiple back-end X servers making up a large
    display."""

    homepage = "http://dmx.sourceforge.net/"
    url      = "https://www.x.org/archive/individual/proto/dmxproto-2.3.1.tar.gz"

    version('2.3.1', '7c52af95aac192e8de31bd9a588ce121')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
