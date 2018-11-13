# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Resourceproto(AutotoolsPackage):
    """X Resource Extension.

    This extension defines a protocol that allows a client to query the
    X server about its usage of various resources."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/resourceproto"
    url      = "https://www.x.org/archive/individual/proto/resourceproto-1.2.0.tar.gz"

    version('1.2.0', '33091d5358ec32dd7562a1aa225a70aa')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
