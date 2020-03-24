# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    version('1.0.3', sha256='c1501045ec781f36b6f867611ab2b4e81be542f5c669b2fd0cc4ec1340c42bcf')
