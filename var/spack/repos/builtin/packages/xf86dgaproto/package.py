# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xf86dgaproto(AutotoolsPackage):
    """X.org XF86DGAProto protocol headers."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/xf86dgaproto"
    url      = "https://www.x.org/archive/individual/proto/xf86dgaproto-2.1.tar.gz"

    version('2.1', '1fe79dc07857ad3e1fb8b8f2bdd70d1b')
