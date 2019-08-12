# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xproxymanagementprotocol(AutotoolsPackage):
    """The Proxy Management Protocol is an ICE based protocol that provides a
    way for application servers to easily locate proxy services available to
    them."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/pmproto"
    url      = "https://www.x.org/archive/individual/proto/xproxymanagementprotocol-1.0.3.tar.gz"

    version('1.0.3', 'c4ab05a6174b4e9b6ae5b7cfbb6d718e')
