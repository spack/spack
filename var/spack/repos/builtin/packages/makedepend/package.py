# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Makedepend(AutotoolsPackage):
    """makedepend - create dependencies in makefiles."""

    homepage = "http://cgit.freedesktop.org/xorg/util/makedepend"
    url      = "https://www.x.org/archive/individual/util/makedepend-1.0.5.tar.gz"

    version('1.0.5', 'efb2d7c7e22840947863efaedc175747')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
