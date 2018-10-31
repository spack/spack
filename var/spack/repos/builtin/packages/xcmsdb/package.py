# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xcmsdb(AutotoolsPackage):
    """xcmsdb is used to load, query, or remove Device Color Characterization
    data stored in properties on the root window of the screen as
    specified in section 7, Device Color Characterization, of the
    X11 Inter-Client Communication Conventions Manual (ICCCM)."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xcmsdb"
    url      = "https://www.x.org/archive/individual/app/xcmsdb-1.0.5.tar.gz"

    version('1.0.5', 'e7b1699c831b44d7005bff45977ed56a')

    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
