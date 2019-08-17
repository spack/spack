# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxaw3d(AutotoolsPackage):
    """Xaw3d is the X 3D Athena Widget Set.
    Xaw3d is a widget set based on the X Toolkit Intrinsics (Xt) Library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXaw3d"
    url      = "https://www.x.org/archive/individual/lib/libXaw3d-1.6.2.tar.gz"

    version('1.6.2', 'e51e00b734853e555ae9b367d213de45')

    depends_on('libx11')
    depends_on('libxt')
    depends_on('libxmu')
    depends_on('libxext')
    depends_on('libxpm')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
