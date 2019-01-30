# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Recordproto(AutotoolsPackage):
    """X Record Extension.

    This extension defines a protocol for the recording and playback of user
    actions in the X Window System."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/recordproto"
    url      = "https://www.x.org/archive/individual/proto/recordproto-1.14.2.tar.gz"

    version('1.14.2', '868235e1e150e68916d5a316ebc4ccc4')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
