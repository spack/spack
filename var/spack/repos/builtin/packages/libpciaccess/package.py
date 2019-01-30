# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libpciaccess(AutotoolsPackage):
    """Generic PCI access library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libpciaccess/"
    url      = "http://xorg.freedesktop.org/archive/individual/lib/libpciaccess-0.13.5.tar.gz"

    version('0.13.5', '81468664fde96d1df2c3216fdf3c4a20')
    version('0.13.4', 'cc1fad87da60682af1d5fa43a5da45a4')

    depends_on('libtool', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
