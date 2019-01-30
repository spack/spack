# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xf86rushproto(AutotoolsPackage):
    """X.org XF86RushProto protocol headers."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/xf86rushproto"
    url      = "https://www.x.org/archive/individual/proto/xf86rushproto-1.1.2.tar.gz"

    version('1.1.2', '6a6389473332ace01146cccfef228576')
