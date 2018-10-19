# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Windowswmproto(AutotoolsPackage):
    """This module provides the definition of the WindowsWM extension to the
    X11 protocol, used for coordination between an X11 server and the
    Microsoft Windows native window manager.

    WindowsWM is only intended to be used on Cygwin when running a
    rootless XWin server."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/windowswmproto"
    url      = "https://www.x.org/archive/individual/proto/windowswmproto-1.0.4.tar.gz"

    version('1.0.4', '558db92a8e4e1b07e9c62eca3f04dd8d')
