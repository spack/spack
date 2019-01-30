# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxfixes(AutotoolsPackage):
    """This package contains header files and documentation for the XFIXES
    extension.  Library and server implementations are separate."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXfixes"
    url      = "https://www.x.org/archive/individual/lib/libXfixes-5.0.2.tar.gz"

    version('5.0.2', '3636e59f8f5fa2e469d556d49f30e98d')

    depends_on('libx11@1.6:')

    depends_on('xproto', type='build')
    depends_on('fixesproto@5.0:', type='build')
    depends_on('xextproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
