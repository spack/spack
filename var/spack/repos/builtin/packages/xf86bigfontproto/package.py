# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xf86bigfontproto(AutotoolsPackage):
    """X.org XF86BigFontProto protocol headers."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/xf86bigfontproto"
    url      = "https://www.x.org/archive/individual/proto/xf86bigfontproto-1.2.0.tar.gz"

    version('1.2.0', '91b0733ff4cbe55808d96073258aa3d1')
