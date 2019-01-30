# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xf86miscproto(AutotoolsPackage):
    """This package includes the protocol definitions of the "XFree86-Misc"
    extension to the X11 protocol.  The "XFree86-Misc" extension is
    supported by the XFree86 X server and versions of the Xorg X server
    prior to Xorg 1.6."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/xf86miscproto"
    url      = "https://www.x.org/archive/individual/proto/xf86miscproto-0.9.3.tar.gz"

    version('0.9.3', 'c6432f04f84929c94fa05b3a466c489d')
