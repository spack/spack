# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xextproto(AutotoolsPackage):
    """X Protocol Extensions."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/xextproto"
    url      = "https://www.x.org/archive/individual/proto/xextproto-7.3.0.tar.gz"

    version('7.3.0', '37b700baa8c8ea7964702d948dd13821')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    parallel = False
