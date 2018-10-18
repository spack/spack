# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Renderproto(AutotoolsPackage):
    """X Rendering Extension.

    This extension defines the protcol for a digital image composition as
    the foundation of a new rendering model within the X Window System."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/renderproto"
    url      = "https://www.x.org/archive/individual/proto/renderproto-0.11.1.tar.gz"

    version('0.11.1', '9b103359123e375bb7760f7dbae3dece')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
