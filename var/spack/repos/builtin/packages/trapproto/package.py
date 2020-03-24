# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Trapproto(AutotoolsPackage):
    """X.org TrapProto protocol headers."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/trapproto"
    url      = "https://www.x.org/archive/individual/proto/trapproto-3.4.3.tar.gz"

    version('3.4.3', sha256='abfb930b5703b5a6ebafe84d0246bd8c6b099ca4a4eab06d1dc0776a8a9b87c1')
