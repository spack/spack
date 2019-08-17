# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Grandr(AutotoolsPackage):
    """RandR user interface using GTK+ libraries."""

    homepage = "https://cgit.freedesktop.org/xorg/app/grandr"
    url      = "https://www.x.org/archive/individual/app/grandr-0.1.tar.gz"

    version('0.1', '707109a105f2ab1bb216e6e6a5a10ba4')

    depends_on('gtkplus@2.0.0:')
    depends_on('gconf')
    depends_on('xrandr@1.2:')
