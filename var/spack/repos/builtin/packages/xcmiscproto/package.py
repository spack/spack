# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xcmiscproto(AutotoolsPackage):
    """XC-MISC Extension.

    This extension defines a protocol that provides Xlib two ways to query
    the server for available resource IDs."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/xcmiscproto"
    url      = "https://www.x.org/archive/individual/proto/xcmiscproto-1.2.2.tar.gz"

    version('1.2.2', 'ded6cd23fb2800df93ebf2b3f3b01119')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
