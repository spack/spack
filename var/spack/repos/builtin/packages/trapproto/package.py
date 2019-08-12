# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Trapproto(AutotoolsPackage):
    """X.org TrapProto protocol headers."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/trapproto"
    url      = "https://www.x.org/archive/individual/proto/trapproto-3.4.3.tar.gz"

    version('3.4.3', '1344759ae8d7d923e64f5eec078a679b')
